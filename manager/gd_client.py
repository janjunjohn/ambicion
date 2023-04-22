from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError as HTTPError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import os
import io
import shutil
import environ

env = environ.Env()
env.read_env()

SCOPES = ['https://www.googleapis.com/auth/drive']
GALLERY_FOLDER = {'name': 'gallery', 'gd_id': env('GD_GALLERY_FOLDER_ID')}
SAMPLE_FOLDER = {'name': 'sample', 'gd_id': env('GD_SAMPLE_FOLDER_ID')}
FAMILY_FOLDER = {'name': 'family', 'gd_id': env('GD_FAMILY_FOLDER_ID')}
FOLDER_LIST = [GALLERY_FOLDER, SAMPLE_FOLDER, FAMILY_FOLDER]


class GoogleDriveClient:
    def __init__(self):
        self.scopes = SCOPES
        sa_creds = service_account.Credentials.from_service_account_file(
            'service_account.json'
        )
        scoped_creds = sa_creds.with_scopes(self.scopes)
        self.service = build('drive', 'v3', credentials=scoped_creds)

    def download_all_files(self):  # google drive上の全ての画像ファイルをherokuサーバーにダウンロード
        for parents_folder in FOLDER_LIST:
            parents_folder_name = parents_folder['name']
            parents_folder_id = parents_folder['gd_id']

            response = (
                self.service.files()
                .list(
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                    q=f'parents in "{parents_folder_id}" and trashed = false',
                    fields='nextPageToken, files(id, name)',
                )
                .execute()
            )
            all_target_files = response['files']
            for target_file in all_target_files:
                target_file_name = target_file['name']
                target_file_id = target_file['id']

                request = self.service.files().get_media(fileId=target_file_id)
                fh = io.FileIO(target_file_name, mode='wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    if status:
                        print('Download %d%%.' % int(status.progress() * 100))
                print(f'{target_file_name}: Download Complete!')
                shutil.move(
                    target_file_name, 'media/' + parents_folder_name
                )  # 対象のパスに移動: media/sample, gallery or family/

    def upload_file(self, file_path, folder_name):
        upload_file_name = os.path.basename(file_path)
        mine_type = 'media/png'
        for parents_folder in FOLDER_LIST:
            if parents_folder['name'] == folder_name:
                parents_folder_id = parents_folder['gd_id']
        
        file_path = file_path[1:]  # MediaFileUploadに合わせ、先頭の"/"を削除
        media = MediaFileUpload(file_path, mimetype=mine_type, resumable=True)
        file_metadata = {
            'name': upload_file_name,
            'mimeType': mine_type,
            'parents': [parents_folder_id],
        }
        uploaded_file = (
            self.service.files().create(body=file_metadata, media_body=media).execute()
        )
        print(f'upload file completed. <{uploaded_file["name"]}>')

    def delete_file(self, file_name, folder_name):
        file_name = file_name.replace(f'{folder_name}/', '')
        for parents_folder in FOLDER_LIST:
            if parents_folder['name'] == folder_name:
                parents_folder_id = parents_folder['gd_id']
        file_query = f'name="{file_name}" and parents in "{parents_folder_id}"'
        file_results = (
            self.service.files()
            .list(q=file_query, fields='nextPageToken, files(id, name)')
            .execute()
        )
        files = file_results.get('files', [])
        target_file_id = files[0]['id']
        if target_file_id:
            self.service.files().delete(fileId=target_file_id).execute()
            print(f'delete file completed. <{files[0]["name"]}>')

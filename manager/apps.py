from django.apps import AppConfig


class ManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "manager"

    def ready(self):
        import json
        from .gd_client import GoogleDriveClient
        import environ
        import os


        env = environ.Env()
        env.read_env()
        
        path = 'service_account.json'
        is_file = os.path.isfile(path)

        if not is_file:  # ready()が複数回実行された場合にスキップする(既に実行された場合は’service_account.json’は既に存在する)
            SERVICE_ACCOUNT_DICT = {
                "type": "service_account",
                "project_id": "ambicion-jp",
                "private_key_id": env("GD_PRIVATE_KEY_ID"),
                "private_key": env("GD_PRIVATE_KEY").replace('\\n', '\n'),
                "client_email": env("GD_CLIENT_EMAIL"),
                "client_id": env("GD_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": env("GD_CERT_URL"),
            }

            with open("service_account.json", "w") as f:
                json.dump(SERVICE_ACCOUNT_DICT, f)

            gdc = GoogleDriveClient()
            gdc.download_all_files()

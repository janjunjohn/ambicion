import requests
import environ
from client.models import LineUser
from django.db.utils import IntegrityError


env = environ.Env()
environ.Env.read_env()


class LINE_API_Service:
    _LIMIT_COUNT = 200

    def __init__(self, token: str, secret: str) -> None:
        self.token = token
        self.secret = secret

    def _check_signature(self, request) -> bool:
        import hmac
        import hashlib
        import base64

        channel_secret = self.secret.encode('utf-8')
        signature = request.headers.get('X-Line-Signature', '')
        body = request.body

        hash = hmac.new(channel_secret, body, hashlib.sha256).digest()
        expected_signature = base64.b64encode(hash).decode('utf-8')

        return hmac.compare_digest(signature, expected_signature)

    def _get_consumption(self) -> int:
        """
        今月送った通数を取得
        """
        r = requests.get(
            "https://api.line.me/v2/bot/message/quota/consumption", headers={"Authorization": f"Bearer {self.token}"}
        )
        r.raise_for_status()
        return r.json()["consumption"]

    def send_line_message(self, user_id: str, message: str) -> bool:
        """
        LINE Messaging APIでメッセージを送信
        """
        consumption: int = self._get_consumption()
        if consumption >= self._LIMIT_COUNT:
            print("LINE message limit reached for this month.")
            return False
        message_no = consumption + 1
        message_with_count = f"[{message_no}/{self._LIMIT_COUNT}]\n {message}"
        url = "https://api.line.me/v2/bot/message/push"
        body = {
            "to": user_id,
            "messages": [{"type": "text", "text": message_with_count}]
        }

        try:
            r = requests.post(url, headers={"Authorization": f"Bearer {self.token}"}, json=body)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"LINE message sending failed: {e}")
            return False
        return True

    def add_line_user(self, user_id: str, name: str) -> bool:
        try:
            user = LineUser(user_id=user_id, name=name)
            user.save()
        except IntegrityError:
            return self.send_line_message(user_id, "その名前は既に登録されています。")

        return self.send_line_message(user_id, "登録完了！")
    
    def update_receiver_status(self, user_id: str) -> bool:
        try:
            receiver = LineUser.objects.filter(is_receiver=True).first()
            if receiver:
                receiver.is_receiver = False
                receiver.save()

            user_update = LineUser.objects.get(user_id=user_id)
            user_update.is_receiver = True
            user_update.save()
            assert LineUser.objects.filter(is_receiver=True).count() == 1
            return self.send_line_message(user_id, "あなたを新しい受信者に設定しました！")
        except Exception:
            return self.send_line_message(user_id, "受信者の更新に失敗しました。")

    def get_line_user_list(self, user_id: str) -> bool:
        try:
            user_list = LineUser.objects.values_list('name', 'is_receiver')
            user_list_text = '\n'.join([name if not is_receiver else name + ' (受信者)' for name, is_receiver in user_list])
            message = "ユーザー一覧:\n" + user_list_text
            return self.send_line_message(user_id, message)
        except LineUser.DoesNotExist:
            return self.send_line_message(user_id, "ユーザーが存在しません。")
        except Exception:
            return self.send_line_message(user_id, "ユーザー一覧の取得に失敗しました。")

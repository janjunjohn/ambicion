import requests
import environ
from client.models import LineUser
from django.db.utils import IntegrityError


env = environ.Env()
environ.Env.read_env()


class MessageConsumptionLimitError(Exception):
    pass


class LINE_API_Service:
    _LIMIT_COUNT = 200

    def __init__(self, account: str, token: str, secret: str) -> None:
        self.account: str = account
        self.token: str = token
        self.secret: str = secret

    def _check_signature(self, request: requests.Request) -> bool:
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
        return r.json()["totalUsage"]

    def get_receiver_user_id(self) -> LineUser | None:
        """
        受信者ユーザーを取得
        """
        receiver = LineUser.objects.filter(account=self.account, is_receiver=True).first()
        return receiver.user_id if receiver else None

    def send_line_message(self, user_id: str, message: str) -> bool:
        """
        LINE Messaging APIでメッセージを送信
        """
        consumption: int = self._get_consumption()
        if consumption >= self._LIMIT_COUNT:
            print("LINE message limit reached for this month.")
            raise MessageConsumptionLimitError("LINE message limit reached for this month.")

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
        print("LINE message sent successfully.")
        return True

    def add_line_user(self, user_id: str, name: str) -> bool:
        try:
            user = LineUser(account=self.account, user_id=user_id, name=name)
            user.save()
        except IntegrityError:
            return self.send_line_message(user_id, "その名前は既に使用されているか、 ユーザーがすでに存在します。")

        return self.send_line_message(user_id, "登録完了！")

    def update_receiver_status(self, user_id: str) -> bool:
        try:
            receiver = LineUser.objects.filter(account=self.account, is_receiver=True).first()
            if receiver:
                receiver.is_receiver = False
                receiver.save()

            user_update = LineUser.objects.get(account=self.account, user_id=user_id)
            user_update.is_receiver = True
            user_update.save()
            assert LineUser.objects.filter(account=self.account, is_receiver=True).count() == 1
            return self.send_line_message(user_id, "あなたを新しい受信者に設定しました！")
        except Exception:
            return self.send_line_message(user_id, "受信者の更新に失敗しました。")

    def get_line_user_list(self, user_id: str) -> bool:
        try:
            user_list = LineUser.objects.filter(account=self.account).values_list('name', 'is_receiver')
            user_list_text = '\n'.join(
                [name if not is_receiver else name + ' (受信者)' for name, is_receiver in user_list]
            )
            message = "ユーザー一覧:\n" + user_list_text
            return self.send_line_message(user_id, message)
        except Exception:
            return self.send_line_message(user_id, "ユーザー一覧の取得に失敗しました。")

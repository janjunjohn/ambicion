from datetime import datetime
import json
from django.http import HttpResponse
import environ
import requests

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.core.mail import send_mail

from client.services.line_api_service import LINE_API_Service, MessageConsumptionLimitError

from .models import Gallery, Sample, Family
from .services.instagram_api_service import InstagramAPIService

# Set Environment Variables
env = environ.Env()
environ.Env.read_env()


PYTHON_EMAIL = env('PYTHON_EMAIL')
AMBICION_EMAIL = env('AMBICION_EMAIL')
SECRET_KEY = env('SECRET_KEY')
TURNSTILE_SITEKEY = env('TURNSTILE_SITEKEY')
TURNSTILE_SECRET_KEY = env('TURNSTILE_SECRET_KEY')
BLOCK_LIST = env('BLOCK_LIST')


def validate_turnstile(token, secret, remoteip=None):
    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'

    data = {
        'secret': secret,
        'response': token
    }

    if remoteip:
        data['remoteip'] = remoteip

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Turnstile validation error: {e}")
        return {'success': False, 'error-codes': ['internal-error']}


class TopView(TemplateView):
    template_name = 'client/index.html'
  
    def get_context_data(self, **kwargs):
        current_year = datetime.now().year
        context = super().get_context_data(**kwargs)
        context['year'] = current_year
        context['gallery_list'] = Gallery.objects.filter(is_standby=False).all()
        context['sample_list'] = Sample.objects.filter(is_standby=False).all()
        context['turnstile_sitekey'] = TURNSTILE_SITEKEY
        # instagramの投稿を取得
        instagram_post_list = InstagramAPIService.get_recent_posts(post_num=9)
        context['instagram_post_list'] = instagram_post_list
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        token = request.POST.get('cf-turnstile-response')
        remoteip = request.headers.get('CF-Connecting-IP') or \
            request.headers.get('X-Forwarded-For') or \
            request.remote_addr

        validation = validate_turnstile(token, TURNSTILE_SECRET_KEY, remoteip)
        if validation['success']:
            username = request.POST.get('username')
            user_email = request.POST.get('email')
            free_text = request.POST.get('free-text')
            message = "お問い合わせ内容\n"
            message += free_text + "\n\n"
            message += f'お名前: {username} \n'
            message += f'Email: {user_email} \n'
            if not user_email in BLOCK_LIST:
                line_token = env("LINE_TOKEN_ALPHA")
                line_secret = env("LINE_SECRET_ALPHA")
                line_service = LINE_API_Service(account="alpha", token=line_token, secret=line_secret)

                receiver_line_user_id = line_service.get_receiver_user_id()
                try:
                    _ = line_service.send_line_message(
                        user_id=receiver_line_user_id,
                        message=message
                    )
                    context['submitted'] = 'success'
                except MessageConsumptionLimitError:
                    line_token = env("LINE_TOKEN_BETA")
                    line_secret = env("LINE_SECRET_BETA")
                    line_service = LINE_API_Service(account="beta", token=line_token, secret=line_secret)
                    receiver_line_user_id = line_service.get_receiver_user_id()
                    try:
                        _ = line_service.send_line_message(
                            user_id=receiver_line_user_id,
                            message=message
                        )
                        context['submitted'] = 'success'
                    except Exception:
                        context['submitted'] = 'fail'
                except Exception:
                    context['submitted'] = 'fail'

                context['username'] = username
            else:
                context['submitted'] = 'fail'
        else:
            context['submitted'] = 'fail'
        return render(request, self.template_name, context=context)


class OrderView(TemplateView):
    template_name = 'client/order.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year
        context['year'] = current_year
        context['turnstile_sitekey'] = TURNSTILE_SITEKEY
        context['sample_list'] = Sample.objects.filter(is_standby=False).all()
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        token = request.POST.get('cf-turnstile-response')
        remoteip = request.headers.get('CF-Connecting-IP') or \
            request.headers.get('X-Forwarded-For') or \
            request.remote_addr
       
        validation = validate_turnstile(token, TURNSTILE_SECRET_KEY, remoteip)
        if validation['success']:
            username = request.POST.get('username')
            user_email = request.POST.get('email')
            uniform = request.POST.get('form-uniform')
            socks = request.POST.get('form-socks')
            number = request.POST.get('form-number')
            fabric = request.POST.get('form-fabric')
            neck = request.POST.get('form-neck')
            sleeve = request.POST.get('form-sleeve')
            default = request.POST.get('form-default')
            free_text = request.POST.get('free-text')
            message = '注文が届きました！\n\n'
            message += f'お名前: {username} \n'
            message += f'Email: {user_email} \n'
            message += f'ユニフォーム: {uniform} {socks} \n'
            message += f'枚数: {number} \n'
            message += f'生地: {fabric} \n'
            message += f'襟: {neck} \n'
            message += f'袖: {sleeve} \n'
            message += f'デフォルトデザイン: {default} \n'
            message += f'備考: \n{free_text} \n'
            
            if not user_email in BLOCK_LIST:
                line_token = env("LINE_TOKEN_ALPHA")
                line_secret = env("LINE_SECRET_ALPHA")
                line_service = LINE_API_Service(account="alpha", token=line_token, secret=line_secret)

                receiver_line_user_id = line_service.get_receiver_user_id()
                try:
                    _ = line_service.send_line_message(
                        user_id=receiver_line_user_id,
                        message=message
                    )
                    context['submitted'] = 'success'
                except MessageConsumptionLimitError:
                    line_token = env("LINE_TOKEN_BETA")
                    line_secret = env("LINE_SECRET_BETA")
                    line_service = LINE_API_Service(account="beta", token=line_token, secret=line_secret)
                    receiver_line_user_id = line_service.get_receiver_user_id()
                    try:
                        _ = line_service.send_line_message(
                            user_id=receiver_line_user_id,
                            message=message
                        )
                        context['submitted'] = 'success'
                    except Exception:
                        context['submitted'] = 'fail'
                except Exception:
                    context['submitted'] = 'fail'

                context['username'] = username
            else:
                context['submitted'] = 'fail'
        else:
            context['submitted'] = 'fail'
        return render(request, self.template_name, context=context)


class AboutView(TemplateView):
    template_name = 'client/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year
        context['year'] = current_year
        return context


class FamilyView(TemplateView):
    template_name = 'client/family.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year
        context['year'] = current_year
        context['family_list'] = Family.objects.filter(is_standby=False).all()
        return context


@method_decorator(csrf_exempt, name='dispatch')
class LineWebhookView(TemplateView):
    _ACCOUNT: str
    _LINE_TOKEN: str
    _LINE_SECRET: str

    def setup(self, request, *args, **kwargs):
        """初期化時にトークンとシークレットを設定"""
        super().setup(request, *args, **kwargs)
        self.service = LINE_API_Service(account=self._ACCOUNT, token=self._LINE_TOKEN, secret=self._LINE_SECRET)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        def _handle_service(message: str, user_id: str) -> bool:
            if message == 'list':
                return self.service.get_line_user_list(user_id)
            elif message == 'receiver':
                return self.service.update_receiver_status(user_id)
            elif message.startswith('add '):
                name = message[4:].strip()
                return self.service.add_line_user(user_id, name)
            return False

        if not self.service._check_signature(request):
            return HttpResponse("Invalid signature", status=400)

        body = json.loads(request.body.decode("utf-8"))
        events = body.get("events", [])

        for event in events:
            event_type = event.get("type")  # message / follow / unfollow / postback など
            if event_type != "message":
                continue  # message イベント以外は無視
            message = event.get("message", {})
            user_id = event["source"]["userId"]  # 必ず source から取る
            _ = _handle_service(message.get("text", ""), user_id)
        return HttpResponse("OK")


class LineWebhookDevView(LineWebhookView):
    """開発環境用LINE Webhook"""
    _ACCOUNT = 'dev'
    _LINE_TOKEN = env("LINE_TOKEN_DEV")
    _LINE_SECRET = env("LINE_SECRET_DEV")


class LineWebhookAlphaView(LineWebhookView):
    """ALPHA環境用LINE Webhook"""
    _ACCOUNT = 'alpha'
    _LINE_TOKEN = env("LINE_TOKEN_ALPHA")
    _LINE_SECRET = env("LINE_SECRET_ALPHA")


class LineWebhookBetaView(LineWebhookView):
    """BETA環境用LINE Webhook"""
    _ACCOUNT = 'beta'
    _LINE_TOKEN = env("LINE_TOKEN_BETA")
    _LINE_SECRET = env("LINE_SECRET_BETA")

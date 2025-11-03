from datetime import datetime
import environ
import requests

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.mail import send_mail

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
      message = request.POST.get('free-text')
      if not user_email in BLOCK_LIST:
        send_mail(f'質問：{username} 様',
                  f'お名前: {username} \n' \
                  f'Email: {user_email} \n' \
                  f'備考: {message} \n',
                  PYTHON_EMAIL,
                  [AMBICION_EMAIL],
                  fail_silently=False,
                  )
        context['submitted'] = 'success'
        context['username'] = username
        return render(request, self.template_name, context=context)
      else:
        context['submitted'] = 'fail'
        return render(request, self.template_name, context=context) 
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
      message = request.POST.get('free-text')
      if not user_email in BLOCK_LIST:
        send_mail(f'{username} 様',
                  f'お名前: {username} \n' \
                  f'Email: {user_email} \n' \
                  f'ユニフォーム: {uniform} {socks} \n' \
                  f'枚数: {number} \n' \
                  f'生地: {fabric} \n' \
                  f'襟: {neck} \n' \
                  f'袖: {sleeve} \n' \
                  f'デフォルトデザイン: {default} \n' \
                  f'備考: {message} \n',
                  PYTHON_EMAIL,
                  [AMBICION_EMAIL],
                  fail_silently=False,
                  )
        context['submitted'] = 'success'
        context['username'] = username
        return render(request, self.template_name, context=context)
      else:
        context['submitted'] = 'fail'
        return render(request, self.template_name, context=context) 
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
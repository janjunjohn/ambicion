from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.mail import send_mail
import environ
from .models import Gallery, Sample, Family
from datetime import datetime

# Set Environment Variables
env = environ.Env()
environ.Env.read_env()


PYTHON_EMAIL = env('PYTHON_EMAIL')
AMBICION_EMAIL = env('AMBICION_EMAIL')
SECRET_KEY = env('SECRET_KEY')
RECAPTCHA_SITEKEY = env('RECAPTCHA_SITEKEY')
RECAPTCHA_SECRET_KEY = env('RECAPTCHA_SECRET_KEY')
RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'
BLOCK_LIST = env('BLOCK_LIST')


class TopView(TemplateView):
  template_name = 'client/index.html'
  
  def get_context_data(self, **kwargs):
    current_year = datetime.now().year
    context = super().get_context_data(**kwargs)
    context['year'] = current_year
    context['gallery_list'] = Gallery.objects.filter(is_standby=False).all()
    context['sample_list'] = Sample.objects.filter(is_standby=False).all()
    context['recaptcha_sitekey'] = RECAPTCHA_SITEKEY
    return context
  
  def post(self, request, *args, **kwargs):
    context = self.get_context_data(**kwargs)
    # recaptcha_response = request.POST.get('g-recaptcha-response')
    # is_success_recaptcha = requests.post(url=RECAPTCHA_URL,
    #                                       params={'secret': RECAPTCHA_SECRET_KEY,
    #                                               'response': recaptcha_response}).json()['success']
    is_success_recaptcha = True
    if is_success_recaptcha:
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
    context['recaptcha_sitekey'] = RECAPTCHA_SITEKEY
    context['sample_list'] = Sample.objects.filter(is_standby=False).all()
    return context
  
  def post(self, request, *args, **kwargs):
    context = self.get_context_data(**kwargs)
    # recaptcha_response = request.POST.get('g-recaptcha-response')
    # is_success_recaptcha = requests.post(url=RECAPTCHA_URL,
    #                                       params={'secret': RECAPTCHA_SECRET_KEY,
    #                                               'response': recaptcha_response}).json()['success']
    is_success_recaptcha = True
    if is_success_recaptcha:
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
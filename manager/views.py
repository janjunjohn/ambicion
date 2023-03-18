from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, View
from client.models import Gallery, Sample, Family
from .forms import GalleryForm, SampleForm
from django.contrib import messages



class TopView(TemplateView):
  template_name = 'manager/top.html'
  

class MainSlideView(CreateView):
  template_name = 'manager/main_slide.html'
  form_class = GalleryForm
  
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(**kwargs)
    context['gallery_list'] = Gallery.objects.all()
    context['gallery_count'] = Gallery.objects.count()
    return context
  
  def post(self, request, *args, **kwargs):
    target_pk = request.POST.get('pk')
    target_img = request.FILES.get('img')
    if target_img is None:
      target_img = Gallery.objects.get(pk=target_pk).img
    target_title = request.POST.get('title')
    if target_title == '':
      target_title = Gallery.objects.get(pk=target_pk).title
    try:
      Gallery.objects.update_or_create(pk=target_pk, defaults={'img': target_img, 'title': target_title})
      messages.success(request, '更新完了！')
    except:
      messages.error(request, '同じタイトルは使えない！') 
    return redirect('manager:main_slide')
  

class SampleView(CreateView):
  template_name = 'manager/sample.html'
  form_class = SampleForm
  
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(**kwargs)
    context['sample_list'] = Sample.objects.all()
    return context
  
  def post(self, request, *args, **kwargs):
    target_pk = request.POST.get('pk')
    target_img = request.FILES.get('img')
    if target_img is None:
      target_img = Sample.objects.get(pk=target_pk).img
    target_name = request.POST.get('name')
    if target_name == '':
      target_name = Sample.objects.get(pk=target_pk).name
    try:
      Sample.objects.update_or_create(id=target_pk,  defaults={'img': target_img, 'name': target_name})
      messages.success(request, '更新完了！')
    except:
      messages.error(request, '同じ名前は使えない！')
    return redirect('manager:sample')

  
class FamilyView(CreateView):
  template_name = 'manager/family.html'
  model = Family


class DeleteView(View):
  
  def get(self, request, *args, **kwargs):
    page_name = self.kwargs['page_name']
    target_pk = self.kwargs['pk']
    if page_name == 'main_slide':
      Gallery.objects.get(id=target_pk).delete()
    elif page_name == 'sample':
      Sample.objects.get(id=target_pk).delete()
    elif page_name == 'family':
      Family.objects.get(id='pk').delete()
    return redirect(f'manager:{page_name}')
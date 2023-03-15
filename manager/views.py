from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, View
from client.models import Gallery, Sample, Family
from .forms import GalleryForm, SampleForm


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
      Gallery.objects.update_or_create(id=request.POST.get('pk'), defaults={'title': request.POST.get('title'), 'img': request.FILES.get('img')})
      return redirect('manager:main_slide')
    

class SampleView(CreateView):
  template_name = 'manager/sample.html'
  form_class = SampleForm
  
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(**kwargs)
    context['sample_list'] = Sample.objects.all()
    return context
  
  def post(self, request, *args, **kwargs):
    Sample.objects.update_or_create(id=request.POST.get('pk'))

  
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
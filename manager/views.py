from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
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

  
class FamilyView(CreateView):
  template_name = 'manager/family.html'
  model = Family

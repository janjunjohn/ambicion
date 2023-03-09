from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from client.models import Gallery, Sample, Family
from .forms import GalleryForm


class TopView(TemplateView):
  template_name = 'manager/top.html'
  

class MainSlideView(CreateView):
  template_name = 'manager/main_slide.html'
  form_class = GalleryForm
  
  def get_context_data(self, *args, **kwargs):
    context = super().get_context_data(**kwargs)
    context['gallery_list'] = Gallery.objects.all()
    return context


class SampleView(CreateView):
  template_name = 'manager/sample.html'
  
  
  
class FamilyView(CreateView):
  template_name = 'manager/family.html'
  model = Family

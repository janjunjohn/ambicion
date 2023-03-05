from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from client.models import Gallery, Sample, Family


class TopView(TemplateView):
  template_name = 'manager/top.html'
  

class MainSlideView(ListView):
  template_name = 'manager/main_slide.html'
  model = Gallery


class SampleView(ListView):
  template_name = 'manager/sample.html'
  model = Sample
  
  
class FamilyView(ListView):
  template_name = 'manager/family.html'
  model = Family

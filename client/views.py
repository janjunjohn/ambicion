from django.shortcuts import render
from django.views import View

class TopView(View):
  template_name = 'top.html'
  
from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('main_slide/', views.MainSlideView.as_view(), name='main_slide'),
    path('sample/', views.SampleView.as_view(), name='sample'),
    path('family/', views.FamilyView.as_view(), name='family'),
]
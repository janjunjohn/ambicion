from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('line-webhook/', views.LineWebhookView.as_view(), name='line_webhook'),
]

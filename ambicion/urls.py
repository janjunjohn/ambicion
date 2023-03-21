from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
import environ


env = environ.Env()
environ.Env.read_env()

urlpatterns = [
    path(env('ADMIN_URL') + '/admin/', admin.site.urls),
    path('', include('client.urls')),
    path('manager/', include('manager.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

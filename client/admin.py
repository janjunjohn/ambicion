from django.contrib import admin
from .models import Gallery, Sample, Family
from manager.models import User

# Register your models here.
admin.site.register(Gallery)
admin.site.register(Sample)
admin.site.register(Family)
admin.site.register(User)

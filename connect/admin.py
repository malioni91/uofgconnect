from django.contrib import admin
from connect.models import Map, Course, UserProfile

# Register your models here.
admin.site.register(Map)
admin.site.register(Course)
admin.site.register(UserProfile)
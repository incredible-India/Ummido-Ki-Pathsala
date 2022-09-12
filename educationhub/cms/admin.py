from django.contrib import admin
from .models import teacher,course

# Register your models here.
@admin.register(teacher)
class teacherADMIN(admin.ModelAdmin):
    list_display = ['id','name','email','password']


@admin.register(course)
class courseADMIN(admin.ModelAdmin):
    list_display = ['id','cname','user','cimg','slug','disp','dateof']
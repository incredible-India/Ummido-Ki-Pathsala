from django.contrib import admin
from .models import teacher,course,chapter,chapter_content

# Register your models here.
@admin.register(teacher)
class teacherADMIN(admin.ModelAdmin):
    list_display = ['id','name','email','password']


@admin.register(course)
class courseADMIN(admin.ModelAdmin):
    list_display = ['id','cname','user','cimg','slug','disp','dateof']




@admin.register(chapter)
class chapterADMIN(admin.ModelAdmin):
    list_display = ['id','title','user','chimg','slug','disp','dateof','course','chfiles','chnumber']


@admin.register(chapter_content)
class chapter_contentADMIN(admin.ModelAdmin):
    list_display = ['id','title','chimg','dispcription','chapter','chfiles']
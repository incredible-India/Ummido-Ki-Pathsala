
from django.db import models
import datetime
from autoslug import AutoSlugField
# Create your models here.
class teacher(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250,unique=True)
    password = models.CharField(max_length=250)



class course(models.Model):
    cname = models.CharField(max_length=400)
    user = models.ForeignKey(teacher,on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='cname',max_length=250,unique=True,null=True,default=None)
    disp = models.TextField(default=False)
    dateof  = models.DateTimeField(auto_now_add=True)
    cimg = models.ImageField(upload_to='courseimg/' ,default=False)



class chapter(models.Model):
    course = models.ForeignKey(course,on_delete=models.CASCADE,related_name='course')
    user = models.ForeignKey(teacher, on_delete=models.CASCADE,related_name='user')
    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='title',unique=True)
    disp = models.TextField()
    chimg = models.ImageField(upload_to='chaptersimg/',default=False)
    chfiles = models.FileField(upload_to='chfiles/',default=False)
    chnumber = models.IntegerField()
    dateof  = models.DateTimeField(auto_now_add=True)



class chapter_content(models.Model):
    title = models.CharField(max_length=250)
    chapter = models.ForeignKey(chapter,on_delete=models.CASCADE)
    dispcription = models.TextField(blank=True)
    chimg = models.ImageField(upload_to='chaptersimg/',default=False)
    chfiles = models.FileField(upload_to='chfiles/',default=False)


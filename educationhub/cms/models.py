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
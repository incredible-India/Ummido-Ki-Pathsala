from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import teacher,course
from .middleware import teacherAuth
from django.utils.decorators import method_decorator
# Create your views here.



class login(View):
    @method_decorator(teacherAuth)
    def get(self,request):
        if request.isauth:
            return HttpResponseRedirect('/cms/home/')
        else:
            return render(request,'cms/login.html')
    
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        isuser = teacher.objects.filter(Q(email=email) & Q(password=password))

        if isuser.exists():

            name = teacher.objects.get(email=email).name

            request.session['email'] = email
            request.session['name'] = name
            return HttpResponseRedirect('/cms/home/')
        else:
            messages.error(request,'Invalid cradential')
            return HttpResponseRedirect('/cms/login/')

class index(View):
    @method_decorator(teacherAuth)
    def get(self,request):
        if request.isauth:
            return HttpResponseRedirect('/cms/home/')
        else:

            return render(request,'cms/create.html')

    def post(self,request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        isExist = teacher.objects.filter(email=email).exists()

        if isExist:
            messages.success(request,'Email Already Exist')
            return render(request,'cms/create.html')

        else:
            teacher.objects.create(name=name,email=email,password=password)

            request.session['email'] =email
            request.session['name'] =name

            return HttpResponseRedirect('/cms/home/')


class home(View):
    @method_decorator(teacherAuth)
    def get(self, request):
        if request.isauth: 

            data = teacher.objects.filter(Q(email = request.session['email']) & Q(name = request.name))

            if data.exists():

                courses = course.objects.filter(user = teacher.objects.get(email = request.session['email']))



                return render(request,'cms/homecms.html',{'data':data,'course':courses})
            else:
                return render(request,'cms/login.html') 
        else:
            return render(request,'cms/login.html')




class logout(View):
    @method_decorator(teacherAuth)
    def get(self, request):
        if request.isauth:
            del request.session['email']
            del request.session['name']
            return HttpResponseRedirect('/')
        else:
            return render(request,'cms/login.html')
        


#adding the course and title to the

class addcourse(View):
    @method_decorator(teacherAuth)
    def get(self, request):
        if request.isauth:
            return render(request,'cms/addcourse.html',{'uname': request.name})
        else:
            return render(request,'cms/addcourse.html')
    
    def post(self, request):
        cname = request.POST.get('cname')
        disp = request.POST.get('disp')
        

        if cname.strip() == '':
            messages.info(request,'Course name cannot be blank')
            return HttpResponseRedirect('/cms/addcourse/')

        if 'cimg' in request.FILES:
            img =  request.FILES['cimg']
        else:
            img=False

        

        course.objects.create(cname=cname,cimg=img,disp=disp,user = teacher.objects.get(email=request.session['email']))

        return HttpResponseRedirect('/cms/home/')



class deleteCourse(View):
    
    def get(self, request,book):
        if 'email' in request.session:
            if 'name' in request.session:
                name = request.session['name']
                email = request.session['email']

                isexist = teacher.objects.filter(Q(email=email) & Q(name=name)).exists()

                if isexist:

                    course.objects.filter(slug=book).delete()
                    return HttpResponseRedirect('/cms/home/')
                else:
                    return HttpResponse('Invalid Request')
            else:
                return render(request,'cms/login.html')
        else:
             return render(request,'cms/login.html')

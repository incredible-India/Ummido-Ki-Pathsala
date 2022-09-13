from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import chapter_content, teacher,course,chapter
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

                    course.objects.filter(Q(slug=book) & Q(user= teacher.objects.get(email=email))).delete()
                    return HttpResponseRedirect('/cms/home/')
                else:
                    return HttpResponse('Invalid Request')
            else:
                return render(request,'cms/login.html')
        else:
             return render(request,'cms/login.html')


class openCourse(View):
    def get(self, request,book):
        if 'email' in request.session:
            if 'name' in request.session:
                name = request.session['name']
                email = request.session['email']

                isexist = teacher.objects.filter(Q(email=email) & Q(name=name)).exists()

                if isexist:
                    courses = course.objects.filter(Q(slug=book) & Q(user= teacher.objects.get(email=email)))

                    if courses.exists():
                        chpaters = chapter.objects.filter( Q(user = teacher.objects.get(email= request.session['email'])) & Q(course = course.objects.get(slug=book)))
                        return render(request, 'cms/course.html',{
                            'name' :name,'email' :email,'course':courses,'chapters':chpaters,'ch':True,'subjectslug':book
                        })
                    else:
                        return HttpResponse('invalid request')
                else:
                    return render(request,'cms/login.html')
            else:
                return render(request,'cms/login.html')
        else:
            return render(request,'cms/login.html')


#addChapter
class addChapter(View):
    def get(self, request,book):
        if 'email' in request.session:
            if 'name' in request.session:
                name = request.session['name']
                email = request.session['email']

                isexist = teacher.objects.filter(Q(email=email) & Q(name=name)).exists()

                if isexist:
                    
                    iscourse = course.objects.filter(Q(slug=book) & Q(user = teacher.objects.get(email= request.session['email']))).exists()

                   #chapters your

                    
                
                    if iscourse:
                        subject = course.objects.get(slug=book) 
                        

                   

                        return render(request,'cms/addchapter.html',{
                            'name':name,
                            'email':email,
                            'subject':subject.cname,
                          
                        })
                    else:
                        return HttpResponse('Invalid Request')

                else:
                    return render(request,'cms/login.html')
            else:
                return render(request,'cms/login.html')
        else:
            return render(request,'cms/login.html')
    def post(self, request,book):
        number = request.POST.get('number')
        title = request.POST.get('title')
        disp = request.POST.get('disp')

        if 'chimg'  in request.FILES:
            img = request.FILES['chimg']
        else:
            img=False
        if 'chfiles'  in request.FILES:
            file = request.FILES['chfiles']
        else:
            file = False
        
        if number =='':
            messages.info(request,'Please enter chapter number')
            return HttpResponseRedirect(f'/cms/add/chapter/{book}/')
            
        if title == '':
            messages.info(request,'Please enter title of chapter  ')
            return HttpResponseRedirect(f'/cms/add/chapter/{book}/')

        if disp.strip() == '':
            dispcription='Not Available'
        else:
            dispcription =disp
        

        chapter.objects.create(title=title,chnumber=number,disp=dispcription,chimg=img,chfiles=file,user = teacher.objects.get(email= request.session['email']),course=course.objects.get(slug=book))

        return HttpResponseRedirect(f'/cms/open/{book}/')


class openChapter(View):
    def get(self, request,book,chapterslug):
        if 'email' in request.session:
            if 'name' in request.session:
                name = request.session['name']
                email = request.session['email']

                isexist = teacher.objects.filter(Q(email=email) & Q(name=name)).exists()

                if isexist:
                    
                    courses = course.objects.filter(Q(slug=book) & Q(user= teacher.objects.get(email=email)))

                   #chapters your
                    if courses.exists():
                        chpaters = chapter.objects.filter(Q(user = teacher.objects.get(email= request.session['email'])) & Q(course = course.objects.get(slug=book)))

                        chapterdata = chapter.objects.filter(Q(slug=chapterslug) & Q(user = teacher.objects.get(email= request.session['email'])) & Q(course = course.objects.get(slug=book)))

                        coursename =course.objects.get(slug=book)

                        #checking the related content for this chapter     

                        contents = chapter_content.objects.filter(chapter=chapter.objects.get(slug=chapterslug))
                        

                        print(contents)
                        return render(request, 'cms/course.html',{
                            'name' :name,'email' :email,'course':courses,'chapters':chpaters,'ch':False,'subjectslug':book,'chapterdata':chapterdata,'coursename' : coursename.cname,
                            'contents':contents
                            })

                    else:
                        return HttpResponse('Invalid request')

                    
                
                  
                else:
                    return render(request,'cms/login.html')
            else:
                return render(request,'cms/login.html')
        else:
            return render(request,'cms/login.html')





class deleteChapter(View):
    def get(self, request,id,book):
        if 'email' in request.session:
            if 'name' in request.session:
                name = request.session['name']
                email = request.session['email']

                isexist = teacher.objects.filter(Q(email=email) & Q(name=name)).exists()

                if isexist:
                    
                    chapters = chapter.objects.filter(Q(slug =id) & Q(user =  teacher.objects.get(email= request.session['email'])))

                   #chapters your
                    if chapters.exists():
                        
                        chapter.objects.filter(Q(user = teacher.objects.get(email= request.session['email'])) & Q(slug =id)).delete()



                        return HttpResponseRedirect(f'/cms/open/{book}/')
                    

                    else:
                        return HttpResponse('Invalid request')

                    
                
                  
                else:
                    return render(request,'cms/login.html')
            else:
                return render(request,'cms/login.html')
        else:
            return render(request,'cms/login.html')






class addcontent(View):
    def get(self, request,id,book):
        if 'email' in request.session:
            if 'name' in request.session:
                name = request.session['name']
                email = request.session['email']

                isexist = teacher.objects.filter(Q(email=email) & Q(name=name)).exists()

                if isexist:
                    
                    chapters = chapter.objects.filter(Q(slug =id) & Q(user =  teacher.objects.get(email= request.session['email'])))

                   #chapters your
                    if chapters.exists():

                        bookname = course.objects.filter(Q(slug =book))

                        if bookname.exists():
                            bname = course.objects.get(slug =book)
                            cname =   chapter.objects.get(slug =id).title

                            return render(request, 'cms/addcontent.html',{
                            'name' :name,'email' :email,'bookname' :bname.cname, 'chname' :cname,
                                })
                        else:
                            return HttpResponse('This book dose not exist')
                    

                    else:
                        return HttpResponse('Invalid request')

                    
                
                  
                else:
                    return render(request,'cms/login.html')
            else:
                return render(request,'cms/login.html')
        else:
            return render(request,'cms/login.html')

    def post(self, request,id,book):
        title = request.POST.get('title')
        dispcription = request.POST.get('disp')

        if 'chimg'  in request.FILES:
            img = request.FILES['chimg']
        else:
            img=False
        if 'chfiles'  in request.FILES:
            file = request.FILES['chfiles']
        else:
            file = False

        if dispcription.strip() == '': 
            disp = 'Not Available'
        else:
            disp = dispcription

        if title.strip() =='':
          
            messages.info(request,'Enter the title')
            return HttpResponseRedirect(f'/cms/add/chapter/content/{id}/{book}/')
    
        
        

        chapter_content.objects.create(title=title,dispcription=disp,chimg=img,chfiles=file,chapter=chapter.objects.get(slug=id))


        return HttpResponseRedirect(f'/cms/open/chapter/{book}/{id}/')

    
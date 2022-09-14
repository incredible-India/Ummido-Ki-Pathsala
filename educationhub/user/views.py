from django.shortcuts import render,HttpResponse
from django.db.models import Q
from django.views import View
from cms.models import course,chapter,chapter_content
# Create your views here.


class index(View):
    def get(self, request):

        courses = course.objects.all()
        return render(request,'index.html',{'courses': courses})



class openCourse(View):
    def get(self, request,id):
        isCourse = course.objects.filter(slug=id)

        if isCourse.exists():
            chapters = chapter.objects.filter(course = course.objects.get(slug=id))
            coursename = course.objects.get(slug=id)
            return render(request,'openchapter.html',{'chapters': chapters,'ch':True,'course':coursename})
        else:
            return HttpResponse('No Course Exist')


class openChapter(View):
    def get(self, request,cid,id):
        isCourse = course.objects.filter(slug=cid)
        MediatypeContent = False
        MediaContentType = []
        if isCourse.exists():

            ischapter = chapter.objects.filter(slug=id)
            if ischapter.exists():

                coursename = course.objects.get(slug=cid)

                chapters = chapter.objects.filter(course = course.objects.get(slug=cid))

                perticularChapter = chapter.objects.filter(Q(course = course.objects.get(slug=cid)) & Q(slug=id))

                if perticularChapter.exists():
                
                    for i in perticularChapter:
                        if i.chfiles != 'False':
                            if str(i.chfiles).endswith('mp4') or str(i.chfiles).endswith('mkv'):
                                MediatypeContent = True
                            else:
                                MediatypeContent =False
                        else:
                            MediatypeContent = False
                else:
                    MediatypeContent = False




                #now time for more content for the related chapter 

                isContent = chapter_content.objects.filter(chapter = chapter.objects.get(slug=id))

                if isContent.exists():
                    for i in isContent:
                        if i.chfiles != 'False':
                            if str(i.chfiles).endswith('mp4') or str(i.chfiles).endswith('mkv'):
                                MediaContentType.append({'types' : 1,'id':i.id })
                            else:
                                MediaContentType.append({'types' : 2,'id':i.id })
                
                

                


                

                        
                
                return render(request,'openchapter.html',{'chapters': chapters,'ch':False,'course':coursename,
                'pchapter':perticularChapter,'type':MediatypeContent,'more':isContent,'ctype':MediaContentType})
            else:
                return HttpResponse('No Chapter Exist',status=404)
        else:
            return HttpResponse('No Course Exist',status=404)
        
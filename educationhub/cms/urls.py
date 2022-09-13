
from django.urls import path,include
from . import views


urlpatterns = [

    path('create/cms/',views.index.as_view(),name='createcms'),
    path('login/',views.login.as_view(),name='logincms'),
    path('logout/',views.logout.as_view(),name='logoutcms'),
    path('home/',views.home.as_view(),name='home'),
    path('addcourse/',views.addcourse.as_view(),name='addcourse'),
    path('delete/<slug:book>/',views.deleteCourse.as_view(),name='deletecourse'),
    path('open/<slug:book>/',views.openCourse.as_view(),name='opencourse'),
    path('add/chapter/<slug:book>/',views.addChapter.as_view(),name='addchapter'),
    path('open/chapter/<slug:book>/<slug:chapterslug>/',views.openChapter.as_view(),name='openchapter'),
    path('delete/chapter/<slug:id>/<slug:book>/',views.deleteChapter.as_view(),name='deletechapter'),
    path('add/chapter/content/<slug:id>/<slug:book>/',views.addcontent.as_view(),name='addcontent')

]

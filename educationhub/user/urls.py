
from django.urls import path,include
from . import views


urlpatterns = [

    path('',views.index.as_view(),name='homepage'),
    path('open/course/<slug:id>/',views.openCourse.as_view(),name='useropencourse'),
    path('open/course/chapter/<slug:cid>/<slug:id>/',views.openChapter.as_view(),name='useropenchapter')

]

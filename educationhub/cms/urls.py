
from django.urls import path,include
from . import views


urlpatterns = [

    path('create/cms/',views.index.as_view(),name='createcms'),
    path('login/',views.login.as_view(),name='logincms'),
    path('logout/',views.logout.as_view(),name='logoutcms'),
    path('home/',views.home.as_view(),name='home'),
    path('addcourse/',views.addcourse.as_view(),name='addcourse'),
    path('delete/<slug:book>/',views.deleteCourse.as_view(),name='deletecourse'),
]

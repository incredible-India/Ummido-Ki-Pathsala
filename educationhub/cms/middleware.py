#checking the user verifications...
#if user is logged in we will show direct profile page and if not we will send response for creating account or login page and
from .models import teacher
from django.db.models import Q
class teacherAuth:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        if 'email' in request.session:
            if 'name' in request.session:
                isExist = teacher.objects.filter(Q(email=request.session['email'])& Q(name=request.session['name']))
                if len(isExist) == 1:
                    request.name = request.session['name']
                    request.email = request.session['email']
                    request.isauth = True
                else:
                    request.isauth = False
                    
            else:
                    request.isauth = False
        else:
                request.isauth = False

        
        response = self.get_response(request)

        return response
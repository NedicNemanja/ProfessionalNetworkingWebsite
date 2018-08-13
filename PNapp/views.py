from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View
from .models import User

# Create your views here.
class welcome(View):
    template_name = 'PNapp/welcome.html'


    def get(self,request):
        return render(request, self.template_name)

    def post(self,request):
        #process post request
        email = request.POST['email']
        password = request.POST['password']
        #querry for user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("No user with email:"+email)
        #autheniticate password
        if user is not None:
            if User.autheniticate(user,password):
                return render(request, 'PNapp/index.html')
            else:
                return HttpResponse("Auth failed")

class Homepage(View):
    def get(self, request):
        return HttpResponse("Homepage")

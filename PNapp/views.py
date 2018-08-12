from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View

# Create your views here.
class welcome(View):
    template_name = 'PNapp/welcome.html'


    def get(self,request):
        return render(request, self.template_name)

    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        '''
        user = autheniticate(username=username,passoword=password)
        if user is None:
            return HttpResponse("Auth failed")
        else
            if user.is_active:
                login(request,user)
                return HttpResponse("Logged in")
        '''
        return HttpResponse(email+password)

class Homepage(View):
    def get(self, request):
        return HttpResponse("Homepage")

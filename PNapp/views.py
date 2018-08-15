from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import View
from .models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

# Create your views here.
class welcome(View):
    template_name = 'PNapp/welcome.html'

    def get(self,request):
        return render(request, self.template_name)

    @method_decorator(csrf_protect)
    def post(self,request):
        #post request for Login existing user
        if request.POST['button'] == "Login":
            #process post request
            email = request.POST['email']
            password = request.POST['password']
            #querry for user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "User with email: "+email+" does not exist")
                return render(request, self.template_name)
            #autheniticate password
            if User.autheniticate(user,password):
                return redirect('index/')
            else:
                messages.error(request, "Wrong Password")
                return render(request, self.template_name)
        #post request for Registering a new user
        elif request.POST['button'] == "Register":
            #process requset
            name = request.POST['name']
            surname = request.POST['surname']
            email = request.POST['email']
            password = request.POST['password']
            confirm = request.POST['confirm']
            if password == confirm:
                #create user
                u = User(name=name, surname=surname, email=email, password=password)
                #make sure the form is correct
                try:
                    u.full_clean()
                except ValidationError as v:
                    messages.error(request, "ValidationError:"+str(v.message_dict))
                    return render(request, self.template_name)
                #save and redirect
                u.save()
                return redirect('index/')
            else:
                messages.error(request, "Passwords don't match")
                return render(request, self.template_name)

class index(View):
    template_name = 'PNapp/index.html'

    def get(self, request):
        return render(request, self.template_name)

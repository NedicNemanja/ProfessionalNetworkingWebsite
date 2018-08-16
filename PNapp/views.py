from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import View
from .models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as site_logout

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
                #create session for this user
                request.session['user_pk'] = user.pk
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
                request.session['user_pk'] = email
                return redirect('index/')
            else:
                messages.error(request, "Passwords don't match")
                return render(request, self.template_name)

class index(View):
    template_name = 'PNapp/index.html'

    def get(self, request):
        user_pk = request.session['user_pk']
        context = {'user_pk':user_pk,}
        return render(request, self.template_name, context=context)

    def post(self, request):
        return render(request, self.template_name)

def logout(request):
    #delete any sessions and cookies
    site_logout(request)
    #return to welcome page
    return redirect('/')

class profile(View):
    template_name = 'PNapp/profile.html'

    def get(self, request):
        #get current user's details
        user_email = request.session['user_pk']
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            messages.error(request, "User with email: "+user_email+" does not exist")
            return render(request, self.template_name)
        user_name = user.name
        user_surname = user.surname
        user_phone = user.phone
        user_photo = user.profile_photo
        user_university = user.university
        user_degree = user.degree_subject
        user_company = user.company
        user_position = user.position

        context = {
        'user_email':user_email,
        'user_name':user_name,
        'user_surname':user_surname,
        'user_phone':user_phone,
        'user_photo':user_photo,
        'user_university':user_university,
        'user_degree':user_degree,
        'user_company':user_company,
        'user_position':user_position,}
        return render(request, self.template_name, context=context)

    def post(self, request):
        return render(request, self.template_name)
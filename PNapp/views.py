from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import View
from .models import User, Post, Connection
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as site_logout
from django.utils import timezone

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
                request.session['user_pk'] = user.id
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
                request.session['user_pk'] = u.id
                return redirect('index/')
            else:
                messages.error(request, "Passwords don't match")
                return render(request, self.template_name)

class index(View):
    template_name = 'PNapp/index.html'

    def get(self, request):
        user = User.objects.get(id=request.session['user_pk'])
        # AXRIASTO AFTO AN VALOUME LOGIN REQUIRE TO LOAD INDEX?
        # try:
        #     user = User.objects.get(email=user.email)
        # except User.DoesNotExist:
        #     messages.error(request, "User with email: "+user.email+" does not exist")
        posts = User.get_posts(user)
        comments_list = []
        for post in posts:
            comments_list.append(Post.get_comments(post))
        #     return render(request, self.template_name)
        #get 9-18 connections
        connections = Connection.objects.filter(receiver=user,accepted=True) | Connection.objects.all().filter(creator=user,accepted=True)
        friends = []
        for conn in connections[:9]:
            if conn.creator == user:
                friends.append(conn.receiver)
            else:
                friends.append(conn.creator)
        context = {'user':user,'friends':friends, 'posts':posts, 'comments_list':comments_list,}
        return render(request, self.template_name, context=context)

    def post(self, request):
        #get current user's details
        user = User.objects.get(id=request.session['user_pk'])
        context = {'user':user,}
        if request.POST["button"] == "Submit status":
            status = request.POST['status']
            p = Post(creator=user, creation_date=timezone.now(), text=status)
            #make sure the form is correct
            try:
                p.full_clean()
            except ValidationError as v:
                messages.error(request, "ValidationError:"+str(v.message_dict))
                return render(request, self.template_name)
            #save and redirect
            p.save()
            return redirect('/index/')
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
        user = User.objects.get(id=request.session['user_pk'])
        # LOGIKA KAI AFT AXRIASTO AN REQUIRE LOGIN?
        # user_id = request.session['user_pk']
        # try:
        #     user = User.objects.get(id=user_id)
        # except User.DoesNotExist:
        #     messages.error(request, "User with email: "+user_email+" does not exist")
        #     return render(request, self.template_name)
        context = {'user':user,}
        return render(request, self.template_name, context=context)

    def post(self, request):
        #get current user's details
        user = User.objects.get(id=request.session['user_pk'])
        # If user pressed save his new details
        new_email = request.POST['email']
        if request.POST["button"] == "Save Changes":
            # If the submitted email is not the one that user had until now
            if user.email != new_email:
                # If the new email is already used
                if User.objects.filter(email=new_email).exists():
                    # Then show message that user with that email already exists
                    messages.error(request, "User with email: " + new_email + " already exists.")
                    return render(request, self.template_name)
            # If password is different from the password's confirmation
            if request.POST['password'] != request.POST['cpassword']:
                messages.error(request, "Passwords should be the same.")
                return render(request, self.template_name)

            # Make the changes he did
            user.name = request.POST['name']
            user.surname = request.POST['surname']
            user.email = request.POST['email']
            user.password = request.POST['password']
            user.phone = request.POST['phone']
            user.university = request.POST['university']
            user.degree_subject = request.POST['degree_subject']
            user.company = request.POST['company']
            user.position = request.POST['position']

            try:
                user.full_clean()
            except ValidationError as v:
                messages.error(request, "ValidationError:"+str(v.message_dict))
                return render(request, self.template_name)

            user.save()
            messages.success(request, "Changes made successfully.")
            return redirect('/profile/')
        return render(request, self.template_name)

class network(View):
    template_name = 'PNapp/network.html'
    def get(self, request):
        #get current user's details
        user = User.objects.get(id=request.session['user_pk'])
        #get all the connections
        connections = Connection.objects.filter(receiver=user,accepted=True) | Connection.objects.all().filter(creator=user,accepted=True)
        friends = []
        for conn in connections:
            if conn.creator == user:
                friends.append(conn.receiver)
            else:
                friends.append(conn.creator)
        context = {'user':user,'friends':friends,}
        return render(request, self.template_name, context=context)

    def post(self, request):
        #get current user's details
        user = User.objects.get(id=request.session['user_pk'])
        context = {'user':user,}
        return render(request, self.template_name, context=context)

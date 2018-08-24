from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views import View
from .models import User, Post, Connection, Comment
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as site_logout
from django.utils import timezone
from itertools import chain

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
                messages.info(request, "User with email: "+email+" does not exist")
                return render(request, self.template_name)
            #autheniticate password
            if User.autheniticate(user,password):
                #create session for this user
                request.session['user_pk'] = user.id
                return redirect('index/')
            else:
                messages.info(request, "Wrong Password")
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
                #validate the model before saving
                try:
                    u.full_clean()
                except ValidationError as v:
                    messages.info(request, "ValidationError:"+str(v.message_dict))
                    return render(request, self.template_name)
                #save and redirect
                u.save()
                request.session['user_pk'] = u.id
                return redirect('index/')
            else:
                messages.info(request, "Passwords don't match")
                return render(request, self.template_name)

class index(View):
    template_name = 'PNapp/index.html'

    def get(self, request):
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')

        posts = User.get_posts(user)
        #get 9-18 connections
        connections = Connection.objects.filter(receiver=user,accepted=True) | Connection.objects.all().filter(creator=user,accepted=True)
        friends = []
        for conn in connections[:9]:
            if conn.creator == user:
                friends.append(conn.receiver)
            else:
                friends.append(conn.creator)
        context = {'user':user,'friends':friends, 'posts':posts,}
        return render(request, self.template_name, context=context)

    def post(self, request):
        #get current user's details
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        context = {'user':user,}
        if request.POST.get("button", False):
            if request.POST["button"] == "Submit status":
                status = request.POST['status']
                p = Post(creator=user, creation_date=timezone.now(), text=status)
                #validate the model before saving
                try:
                    p.full_clean()
                except ValidationError as v:
                    messages.info(request, "ValidationError:"+str(v.message_dict))
                    return render(request, self.template_name)
                #save and redirect
                p.save()
                return redirect('/index/')
        if request.POST.get("comment-button", False):
            post_id = request.POST["comment-button"]
            post = Post.objects.get(pk=post_id)
            text = request.POST['comment']
            c= Comment(creator=user, post_id=post, text=text, creation_date=timezone.now())
            try:
                c.full_clean()
            except ValidationError as v:
                messages.info(request, "ValidationError:"+str(v.message_dict))
                return render(request, self.template_name)
            #save and redirect
            c.save()
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
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        context = {'user':user,}
        return render(request, self.template_name, context=context)

    def post(self, request):
        #get current user's details
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        # If user pressed save his new details
        if request.POST["button"] == "Save Changes":

            # Make the changes he did
            user.name = request.POST['name']
            user.surname = request.POST['surname']
            user.phone = request.POST['phone']
            if request.POST.get("phone_privacy", False):
                user.phone_public = True
            else:
                user.phone_public = False
            user.university = request.POST['university']
            if request.POST.get("university_privacy", False):
                user.university_public = True
            else:
                user.university_public = False
            user.degree_subject = request.POST['degree_subject']
            if request.POST.get("degree_subject_privacy", False):
                user.degree_subject_public = True
            else:
                user.degree_subject_public = False
            user.company = request.POST['company']
            if request.POST.get("company_privacy", False):
                user.company_public = True
            else:
                user.company_public = False
            user.position = request.POST['position']
            if request.POST.get("position_privacy", False):
                user.position_public = True
            else:
                user.position_public = False
            #check if profile photo changes
            if request.FILES.get('image-file',False):
                from django.conf import settings
                from django.core.files.storage import FileSystemStorage
                from django.utils import timezone
                import datetime
                #get image
                myfile = request.FILES['image-file']
                #save image
                fs = FileSystemStorage()
                now = datetime.datetime.now()
                filename = fs.save('profpics/'+now.strftime("%Y/%m/%d//")+str(myfile.name), myfile)
                #change image url in db
                user.profile_photo = fs.url(filename)

            try:
                user.full_clean()
            except ValidationError as v:
                messages.info(request, "ValidationError:"+str(v.message_dict))
                return render(request, self.template_name)

            user.save()
            messages.success(request, "Info updated successfully.")
            return redirect('/profile/')
        return render(request, self.template_name)

class network(View):
    template_name = 'PNapp/network.html'
    def get(self, request):
        #get current user's details
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
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
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        context = {'user':user,}
        return render(request, self.template_name, context=context)


class mymessages(View):
    template_name = 'PNapp/messages.html'

    def get(self, request):
        #test if session active
        try:
            session_test_pk = request.session['user_pk']
        except KeyError:    #user not logged in
            return redirect('/')
        print("here-------------")
        return HttpResponse("Message")


class search(View):
    template_name = 'PNapp/search.html'

    def get(self, request):
        #test if session active
        try:
            session_test_pk = request.session['user_pk']
        except KeyError:    #user not logged in
            return redirect('/')
        query = request.GET["search_text"]
        #if any word of the query is either a name or a surname then add user to set (not case-sensitive)
        users = set()
        for str in query.split():
            result = User.objects.filter(name__icontains=str) | User.objects.filter(surname__icontains=str)
            print(set(result))
            users.update(set(result))
        context = {'users':users,}
        return render(request, self.template_name, context=context)

class overview(View):
    template_name = 'PNapp/overview.html'

    def get(self, request, pk):
        #get current user's details
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        target_user = User.objects.get(id=pk)
        #get all target_user's friends
        friends = set()
        connections = Connection.objects.filter(creator=target_user)
        for conn in connections:    #conns with target as creator
            friends.add(conn.receiver)
        connections = Connection.objects.filter(receiver=target_user)
        for conn in connections:    #conns with target as receiver
            friends.add(conn.creator)
        #get status of friendship in order to decide the context of add button
        connected_users = Connection.objects.filter(creator=user,receiver=target_user,accepted=True).exists() | Connection.objects.filter(creator=target_user,receiver=user,accepted=True).exists()
        request_exists = Connection.objects.filter(creator=user,receiver=target_user).exists() | Connection.objects.filter(creator=target_user,receiver=user).exists()
        context = {'target_user':target_user,'friends':friends, 'connected_users':connected_users,'request_exists':request_exists}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        userid = request.POST['add user']
        receiver = User.objects.get(id=userid)
        try:
            creator = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        print(creator)
        print(receiver)
        conn = Connection.objects.create(creator=creator,receiver=receiver,accepted=False)
        #get all target_user's friends
        friends = set()
        connections = Connection.objects.filter(creator=creator)
        for conn in connections:    #conns with user as creator
            friends.add(conn.receiver)
        connections = Connection.objects.filter(receiver=creator)
        for conn in connections:    #conns with user as receiver
            friends.add(conn.creator)
        #get new context
        context = {'target_user':receiver,'friends':friends, 'connected_users':False,'request_exists':True}
        return render(request, self.template_name, context=context)

class settings(View):
    template_name = 'PNapp/settings.html'

    def get(self, request):
        #get current user's details and check if he is logged in indeed
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        context = {'user':user,}
        return render(request, self.template_name, context=context)

    def post(self, request):
        #get current user's details and check if he is logged in indeed
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        context = {'user':user,}
        # If user pressed save his new credentials
        new_email = request.POST['email']
        if request.POST["button"] == "Save Changes":
            # If the submitted email is not the one that user had until now
            if user.email != new_email:
                # If the new email is already used
                if User.objects.filter(email=new_email).exists():
                    # Then show message that user with that email already exists
                    messages.info(request, "User with email: " + new_email + " already exists.")
                    return render(request, self.template_name)
            # If password is different from the password's confirmation
            if request.POST['password'] != request.POST['cpassword']:
                messages.info(request, "Passwords should be the same.")
                return render(request, self.template_name)

            # Make the changes he did
            user.email = request.POST['email']
            if request.POST.get("email_privacy", False):
                user.email_public = True
            else:
                user.email_public = False
            user.password = request.POST['password']

            try:
                user.full_clean()
            except ValidationError as v:
                messages.info(request, "ValidationError:"+str(v.message_dict))
                return render(request, self.template_name)

            user.save()
            messages.success(request, "Changes made successfully.")
            return redirect('/settings/')
        return render(request, self.template_name, context=context)

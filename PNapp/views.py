from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View
from .models import *
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as site_logout
from django.utils import timezone
from django.template.loader import render_to_string

try:
    from django.utils import simplejson as json
except ImportError:
    import json

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
        #get the [post,total_interests,if user already interested in post] for every post
        posts = User.get_posts(user)
        posts_list = []
        for post in posts:
            posts_list.append([ post,\
                                post.total_interests(),\
                                Interest.objects.filter(creator=user,post=post).exists()])
        #get 9-18 connections
        connections = Connection.objects.filter(receiver=user,accepted=True) | Connection.objects.all().filter(creator=user,accepted=True)
        friends = []
        for conn in connections[:9]:
            if conn.creator == user:
                friends.append(conn.receiver)
            else:
                friends.append(conn.creator)

        context = {'user':user,'friends':friends, 'posts_list':posts_list,'template_name':"index",}
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
        context = {'user':user,'template_name':"profile",}
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
                user.profile_photo = fs.url(filename).replace('media/','')

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
        context = {'user':user,'friends':friends,'template_name':"network",}
        return render(request, self.template_name, context=context)

    def post(self, request):
        #get current user's details
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        context = {'user':user,'template_name':"network",}
        return render(request, self.template_name, context=context)


class mymessages(View):
    template_name = 'PNapp/messages.html'

    def get(self, request, conversation_pk=-1):
        #get current user's details
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        #get conversations
        conversations = user.get_conversations()
        if conversations is not None:
            #get target conversation
            if conversation_pk == -1:
                target_conversation = conversations.first()
            else:
                target_conversation = Conversation.objects.get(id=conversation_pk)
            if target_conversation is not None:
                context = { 'user':user,
                            'conversations':conversations,
                            'target_conversation':target_conversation,
                            'messages':target_conversation.get_messages(),
                            'template_name':"messages",}
                return render(request, self.template_name, context=context)

        return render(request, self.template_name)

    def post(self, request, conversation_pk=-1):
        #get current user's details
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        #new message in chat
        if 'message'in request.POST:
            text=request.POST['message']
            Message.objects.create(text=text,creator=user,conversation=get_object_or_404(Conversation, pk=conversation_pk))
            return redirect('/messages/'+str(conversation_pk))
        #new message from overview (convo might not exist)
        if 'send message' in request.POST:
            target_user=User.objects.get(id=request.POST['send message'])
            #find the conversation between these two
            conversation=Conversation.objects.filter(creator=user,receiver=target_user)\
                       | Conversation.objects.filter(creator=target_user,receiver=user)
            if not conversation:
                #conversation doesnt exist, create
                conversation=Conversation.objects.create(creator=user,receiver=target_user)
                return redirect('/messages/'+str(conversation.id))
            print(conversation)
            return redirect('/messages/'+str(conversation.first().id))

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
        context = { 'user':user, 'target_user':target_user,
                    'friends':friends, 'connected_users':connected_users,
                    'request_exists':request_exists}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        userid = request.POST['add user']
        receiver = User.objects.get(id=userid)
        try:
            creator = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')

        #if 'add user' in request.POST:
        conn = Connection.objects.create(creator=creator,receiver=receiver,accepted=False)
        friends = creator.get_friends() #get all target_user's friends
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
        context = {'user':user,'template_name':"settings",}
        return render(request, self.template_name, context=context)

    def post(self, request):
        #get current user's details and check if he is logged in indeed
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        context = {'user':user,'template_name':"settings",}
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


class ads(View):

    def get(self, request):
        return HttpResponse("ads")


class notifications(View):
    template_name ='PNapp/notifications.html'

    def get(self, request):
        #get current user's details and check if he is logged in indeed
        try:
            user = User.objects.get(id=request.session['user_pk'])
        except KeyError:    #user not logged in
            return redirect('/')
        #friend Requests
        friend_requests = Connection.objects.filter(receiver=user,accepted=False)
        #post notifications
        notifications = user.get_notifications()
        context = {'template_name':"notifications",
                    'friend_requests':friend_requests,
                    'notifications':notifications,
                    'user':user,
                    }
        return render(request, self.template_name, context=context)



##################AJAX VIEWS#############################################
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def interest(request):
    #get current user's details and check if he is logged in indeed
    try:
        user = User.objects.get(id=request.session['user_pk'])
    except KeyError:    #user not logged in
        return redirect('/')
    #get post with pid
    if request.is_ajax():
        postid = request.POST['postid']
        post = get_object_or_404(Post, id=postid)
        #check if this user already expressed interest in this post
        if not Interest.objects.filter(creator=user,post=post).exists():
            print("INterest Create")
            Interest.objects.create(creator=user,post=post,creation_date=timezone.now())
            return JsonResponse({'total_interests': post.total_interests()})
        else:
            return JsonResponse({"error":"User already interested."})
    else:
        return JsonResponse({"error":"request not ajax"})

@csrf_exempt
def friend_request(request):
    #get current user's details and check if he is logged in indeed
    try:
        user = User.objects.get(id=request.session['user_pk'])
    except KeyError:    #user not logged in
        return redirect('/')
    #got a accept/reject on a friendship requets?
    friend_request = Connection.objects.get(id=request.POST['fr_id'])
    if request.POST["action"] == "Accept":
        friend_request.accepted = True
        friend_request.save()
    elif request.POST["action"] == "Reject":
        print("here")
        friend_request.delete()
    return JsonResponse({})

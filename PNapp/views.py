from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def Welcome(request):
    return render(request, 'PNapp/Welcome.html')

def SingIN(request):
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

def SingUP(request):
    return render(request, 'PNapp/SingUP.html')

def Homepage(request):
    return HttpResponse("Homepage")

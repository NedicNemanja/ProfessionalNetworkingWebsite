from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def Welcome(request):
    return HttpResponse("Welcome to Nsite");

def SingIN(request):
    return HttpResponse("SingIN");

def SingUP(request):
    return render(request, 'PNapp/templates/PNapp/SingUP.html')

def Homepage(request):
    return HttpResponse("Homepage");

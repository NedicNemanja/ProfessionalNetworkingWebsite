from django.urls import path
from . import views

urlpatterns = [
    path('', views.Welcome, name='Welcome'),
    path('SingIN/', views.SingIN, name='SingIN'),
    path('SingUP/', views.SingUP, name='SingUP'),
    path('Homepage/', views.Homepage, name='Homepage'),
]

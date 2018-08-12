from django.urls import path
from . import views
from PNapp.views import welcome,Homepage

urlpatterns = [
    path('', welcome.as_view()),
    path('Homepage/', Homepage.as_view()),
]

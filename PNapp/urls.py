from django.urls import path
from . import views
from PNapp.views import welcome, index

urlpatterns = [
    path('', welcome.as_view()),
    path('index/', index.as_view()),
]

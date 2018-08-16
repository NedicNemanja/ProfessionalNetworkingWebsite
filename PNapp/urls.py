from django.urls import path
from . import views
from PNapp.views import welcome, index, profile

urlpatterns = [
    path('', welcome.as_view()),
    path('index/', index.as_view()),
    path('logout/',views.logout, name='logout'),
    path('profile/', profile.as_view()),
]

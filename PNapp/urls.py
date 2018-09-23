from django.urls import path, re_path
from django.conf import settings as django_settings
from django.conf.urls.static import static
from . import views
from PNapp.views import *

urlpatterns = [
    path('', welcome.as_view()),
    #path('<int:>index/', index.as_view()),
    path('index/', index.as_view()),
    path('logout/',views.logout, name='logout'),
    path('profile/', profile.as_view()),
    path('network/', network.as_view()),
    path('messages/', mymessages.as_view()),
    path('messages/<int:conversation_pk>', mymessages.as_view()),
    path('search/', search.as_view()),
    path('overview/<int:pk>', overview.as_view()),
    path('settings/', settings.as_view()),
    path('advertisments/', advertisments.as_view()),
    path('notifications/', notifications.as_view()),
    path('interest/', views.interest, name='interest'),
    path('friend_request/', views.friend_request, name='friend_request'),
    path('new_message/', views.new_message, name='new_message'),

]
#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)

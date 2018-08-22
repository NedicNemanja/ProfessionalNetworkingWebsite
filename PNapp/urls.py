from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from PNapp.views import welcome, index, profile, network, mymessages, search, overview

urlpatterns = [
    path('', welcome.as_view()),
    #path('<int:>index/', index.as_view()),
    path('index/', index.as_view()),
    path('logout/',views.logout, name='logout'),
    path('profile/', profile.as_view()),
    path('network/', network.as_view()),
    path('messages/', mymessages.as_view()),
    path('search/', search.as_view()),
    path('overview/<int:pk>', overview.as_view()),
]
#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from nightlifeapp.views import *
from nightlifeapp import adminpage_urls,user_urls,organizer_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpage/',include(adminpage_urls)),
    path('user/',include(user_urls)),
    path('organizer/',include(organizer_urls)),
    
    
    path('index/', index.as_view(), name='index'),
    path('', usersignup.as_view(),name='usersignup'),
    path('organizersignup', organizersignup.as_view(),name='organizersignup'),
    path('login/', loginview.as_view(),name='login'),
]
# Serve uploaded media files (also when DEBUG=False on Railway)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='ceate-user-token'),
    path('api/', include('account.urls')),
    path('admin/', admin.site.urls)
]
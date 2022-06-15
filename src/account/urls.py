from sys import api_version
from django.urls import path
from .views import UserView

urlpatterns = [
    path('users/new/', UserView.create, name='create-user'),
    path('users/', UserView.list, name='users'),
    path('users/<int:id>/', UserView.get, name='user-by-id'),
    path('users/update/<int:id>/', UserView.update, name='update-user'),
    path('users/login/', UserView.login_user, name='login-user'),
    path('users/logout/', UserView.logout_user, name='logout-user'),
    path('users/add-permission/', UserView.add_permission, name='add-permission'),
]  
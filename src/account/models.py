from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from sqlalchemy import ForeignKey
from .managers import UserManager
from django.utils.translation import ugettext_lazy as _


class UserType(models.Model):
    name = models.CharField(max_length=20,default="")


class CustomUser(AbstractUser):    
    username = None
   
    username = models.CharField(max_length=40, blank=True)
   
    email = models.EmailField(
        "email address",
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
   
    first_name = models.CharField(
        max_length=40,
        default="",
        blank=False
    )
   
    last_name = models.CharField(
        max_length=40,
        default="",
        blank=False
    )

    user_type = models.ForeignKey(
        UserType,on_delete=models.CASCADE,
        null = True
        )

    USERNAME_FIELD = 'email'
   
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
    ]
    objects = UserManager()    
       
    class Meta:
        db_table = 'user'




         
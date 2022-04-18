from django.db import models

from core.models import TimeStamp

class User(TimeStamp):
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    nickname = models.CharField(max_length=40) 
    
    class Meta:
        db_table = 'users'

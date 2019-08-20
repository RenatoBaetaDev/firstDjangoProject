from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=64, blank=True)



class Post(models.Model):
    __tablename__ = 'posts'
    text = models.TextField( )
    timestamp = models.DateTimeField(default=datetime.utcnow)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

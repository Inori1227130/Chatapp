from django.db import models
from django.utils import timezone

class User (models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    password = models.CharField(max_length=20, null=False, blank=False)
    islogin = models.BooleanField(default=False)

class Room (models.Model):
    name = models.TextField(null=False, blank=False)
    
class ChatLog (models.Model):
     room = models.ForeignKey('Room', on_delete=models.PROTECT, null=False)
     user = models.ForeignKey('User', on_delete=models.PROTECT, null=False)
     message = models.TextField(verbose_name='メッセージ', blank=True, null=False)
     date = models.DateTimeField(verbose_name= '投稿日時', default=timezone.now) 
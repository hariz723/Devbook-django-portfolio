from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User,on_delete= models.SET_NULL,null=True)
    topic= models.ForeignKey(Topic,on_delete= models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=False, blank=True)
    participants = models.ManyToManyField(User, related_name='partcipant', blank=True)
    #auto_now value or time change every time user saves
    updated = models.DateTimeField(auto_now=True)
    #auto_now_add value once updated while user first time saves never update again
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    
    def __str__(self) :
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    room = models.ForeignKey(Room,on_delete= models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]
    
    
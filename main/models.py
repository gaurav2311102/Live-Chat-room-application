from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
    
class Room(models.Model):
    
    topics = models.ManyToManyField(Topic,related_name="rooms")
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True) 
    name = models.CharField(max_length=200,)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User,related_name='joined_rooms',through='Membership') 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
 
    class Meta():
        ordering = ['-updated','-created']
        
    def __str__(self):
        return self.name
    
class Message(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    text = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 
    
    
    
    def __str__(self):
        return self.text[:50]
    
class Membership(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints  =[
            models.UniqueConstraint(fields=['user','room'],name='unique membership')
        ]
        
    def __str__(self):
        return f'{self.user.username} in group{self.room.name}'
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_images/',default='profile_images/default.jpg' , blank=True,null=True)
    
    def __str__(self):
        return self.user.username
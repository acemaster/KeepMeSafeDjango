from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phoneNumber = models.CharField(max_length=30)
    collegeName = models.CharField(max_length=128)
    dateOfBirth = models.DateField()
    signUpDate = models.DateField(auto_now=True)
    picture = models.ImageField(upload_to='profile_pictures',blank=True)
    ipaddress = models.URLField(max_length=25)
    lastLoginDate = models.DateTimeField(blank=True)
    status=models.BooleanField(default=False)
    def __unicode__(self):
    	return self.user.first_name


class UserLocation(models.Model):
    user=models.OneToOneField(User)
    latitude=models.CharField(max_length=100)
    longt=models.CharField(max_length=100)
    def __unicode__(self):
        return self.user.first_name


class UserMessages(models.Model):
    userto=models.OneToOneField(User, unique=True, related_name='message_to')
    userfrom=models.OneToOneField(User, unique=True, related_name='message_from')
    messages=models.CharField(max_length=1000)
    message_data=models.DateField(auto_now=True)
    def __unicode__(self):
        return self.userto.first_name


class UserSafetyList(models.Model):
    userto=models.OneToOneField(User, unique=True, related_name='List_to')
    userfrom=models.OneToOneField(User, unique=True, related_name='List_from')
    status=models.IntegerField()
    def __unicode__(self):
        return self.userto.first_name
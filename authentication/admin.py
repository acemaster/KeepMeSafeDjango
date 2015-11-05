from django.contrib import admin
from .models import UserProfile,UserMessages,UserLocation,User

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserLocation)
admin.site.register(UserMessages)

from django.contrib import admin
from .models import UserProfile,UserMessages,UserLocation,User,UserSafetyList,UserNotifications,UserStatus

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserLocation)
admin.site.register(UserMessages)
admin.site.register(UserSafetyList)
admin.site.register(UserNotifications)
admin.site.register(UserStatus)

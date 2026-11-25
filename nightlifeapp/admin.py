from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(usertype)
admin.site.register(UserSignup)
admin.site.register(OrganizerSignup)
admin.site.register(AddEvent)
admin.site.register(Booking)
admin.site.register(Feedback)   
admin.site.register(Notification)
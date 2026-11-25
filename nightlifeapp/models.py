from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date

class usertype(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    type=models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.type
    
    
    
class UserSignup(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    phone=models.CharField(max_length=20,null=True)
    address=models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.user.first_name
   
class OrganizerSignup(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    phone=models.CharField(max_length=20,null=True)
    address=models.CharField(max_length=50,null=True)
    id_proof=models.FileField(null=True)
    image=models.FileField(null=True)
    
    def __str__(self):
        return self.user.first_name

from django.db import models
from django.contrib.auth.models import User
import uuid



class AddEvent(models.Model):

    organizer = models.ForeignKey('OrganizerSignup', on_delete=models.CASCADE, null=True)

    event_name = models.CharField(max_length=100, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()

    location = models.CharField(max_length=150, null=True)

    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    total_tickets = models.IntegerField(default=0)

    description = models.TextField(null=True)

    event_image = models.ImageField(upload_to="events/", blank=True, null=True)

    status = models.CharField(max_length=100, default="pending")

    def __str__(self):
        return f"{self.event_name} - {self.event_date}"


import uuid
class Booking(models.Model):

    user = models.ForeignKey(UserSignup, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(AddEvent, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ticket_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    booking_date = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=20,default="booked")

    def save(self, *args, **kwargs):

        if not self.ticket_id:
            self.ticket_id = "EVT-" + uuid.uuid4().hex[:8].upper()

        super().save(*args, **kwargs)

    def __str__(self):

        if self.user:
            return f"{self.ticket_id} - {self.user.user.username}"

        return self.ticket_id
    
class Feedback(models.Model):

    user = models.ForeignKey(UserSignup, on_delete=models.CASCADE)
    event = models.ForeignKey(AddEvent, on_delete=models.CASCADE)

    rating = models.IntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.event_name} - {self.user.user.username} ({self.rating}⭐)"

class Notification(models.Model):

    user = models.ForeignKey(UserSignup, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

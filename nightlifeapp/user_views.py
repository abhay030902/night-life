from django.shortcuts import render
from django.views.generic import TemplateView,View
from django.contrib.auth.models import User
from flask import request
from nightlifeapp.models import *
from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponse
 
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from nightlifeapp.models import *
from datetime import date


class userhomeview(TemplateView):

    template_name = "user/index.html"

    def get(self, request, *args, **kwargs):

        user = UserSignup.objects.get(user=request.user)

        today = date.today()

        bookings = Booking.objects.filter(user=user, payment_status="paid")

        for booking in bookings:

            event = booking.event

            # calculate remaining days
            days_left = (event.event_date - today).days

            # 5 days before event
            if days_left == 5:

                Notification.objects.get_or_create(
                    user=user,
                    event=booking,
                    message=f"{event.event_name} is happening in 5 days!"
                )

            # 3 days before event
            if days_left == 3:

                Notification.objects.get_or_create(
                    user=user,
                    event=booking,
                    message=f"{event.event_name} is happening in 3 days!"
                )

        notifications = Notification.objects.filter(user=user).order_by("-created_at")

        context = {
            "notifications": notifications,
            "notification_count": notifications.count()
        }

        return render(request, self.template_name, context)    
    
from django.utils import timezone

class viewevent(TemplateView):
    template_name = "user/view_event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()

        event = AddEvent.objects.filter(
            status="approved",
            event_date__gte=today
        )

        context['event'] = event
        return context        
class viewmore_event(TemplateView):
    template_name = "user/viewmore_event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        event_id = self.request.GET.get('id')
        event = AddEvent.objects.get(id=event_id)

        context['event'] = event
        return context        


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse


class book_event(View):

    def get(self, request, *args, **kwargs):

        event_id = request.GET.get('id')
        event = get_object_or_404(AddEvent, id=event_id)

        return render(request, "user/book_event.html", {"event": event})


    def post(self, request, *args, **kwargs):

        event_id = request.POST['event_id']
        quantity = int(request.POST['quantity'])

        return redirect(f"/user/payment?id={event_id}&qty={quantity}")


class payment(View):

    def get(self, request, *args, **kwargs):

        event_id = request.GET.get('id')
        quantity = int(request.GET.get('qty'))

        event = get_object_or_404(AddEvent, id=event_id)

        total = quantity * event.price

        context = {
            "event": event,
            "quantity": quantity,
            "total": total
        }

        return render(request, "user/payment.html", context)


    def post(self, request, *args, **kwargs):

        event_id = request.POST['event_id']
        quantity = int(request.POST['quantity'])

        event = get_object_or_404(AddEvent, id=event_id)

        if event.total_tickets <= 0:
            return HttpResponse("<script>alert('Tickets Sold Out');window.history.back();</script>")

        if quantity <= 0:
            return HttpResponse("<script>alert('Invalid ticket quantity');window.history.back();</script>")

        if quantity > event.total_tickets:
            return HttpResponse("<script>alert('Not enough tickets available');window.history.back();</script>")

        total = quantity * event.price

        booking = Booking()
        booking.user = UserSignup.objects.get(user_id=request.user.id)
        booking.event = event
        booking.quantity = quantity
        booking.total_price = total
        booking.payment_status = "paid"
        booking.save()

        # reduce tickets
        event.total_tickets -= quantity
        event.save()

        return HttpResponse(
            f"<script>alert('Payment Successful! Ticket ID: {booking.ticket_id}');window.location='/user/viewevent_user';</script>"
        )

from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone

from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone

class mytickets(TemplateView):

    template_name = "user/ticket.html"

    def get(self, request, *args, **kwargs):

        user = UserSignup.objects.get(user_id=request.user.id)

        active_tickets = Booking.objects.filter(
            user=user
        ).exclude(payment_status="cancelled").order_by('-id')

        cancelled_tickets = Booking.objects.filter(
            user=user,
            payment_status="cancelled"
        ).order_by('-id')

        bookings = list(active_tickets) + list(cancelled_tickets)

        context = {
            "bookings": bookings,
            "today": timezone.now().date(),
            "now": timezone.now().time()
        }

        return render(request, self.template_name, context)
class give_feedback(TemplateView):
    template_name = "user/feedback.html"

    def get(self, request, *args, **kwargs):

        event_id = request.GET.get("id")
        event = AddEvent.objects.get(id=event_id)

        return render(request, self.template_name, {"event":event})

    def post(self, request, *args, **kwargs):

        event_id = request.POST.get("event_id")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        user = UserSignup.objects.get(user_id=request.user.id)
        event = AddEvent.objects.get(id=event_id)

        Feedback.objects.create(
            user=user,
            event=event,
            rating=rating,
            comment=comment
        )

        return HttpResponse("<script>alert('Feedback submitted');window.location='/user/ticket';</script>")

from datetime import date, datetime
from django.views import View
from django.http import HttpResponse

class cancel_ticket(View):

    def get(self, request):

        booking_id = request.GET.get("id")

        booking = Booking.objects.get(id=booking_id)

        event = booking.event

        today = date.today()
        now = datetime.now().time()

        if event.event_date < today or (event.event_date == today and event.event_time <= now):

            return HttpResponse(
                "<script>alert('Event already started. Ticket cannot be cancelled');window.location='/user/ticket';</script>"
            )

        event.total_tickets += booking.quantity
        event.save()

        booking.payment_status = "cancelled"
        booking.save()

        return HttpResponse(
            "<script>alert('Ticket Cancelled Successfully');window.location='/user/ticket';</script>"
        )
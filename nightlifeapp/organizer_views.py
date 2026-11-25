from django.shortcuts import render
from django.views.generic import TemplateView,View
from django.contrib.auth.models import User
from nightlifeapp.models import *
from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import Sum

class organizerhomeview(TemplateView):
    template_name="organizer/index.html"
class addevent(TemplateView):
    template_name="organizer/add_events.html"

    def post(self, request, *args, **kwargs):

        user = OrganizerSignup.objects.get(user_id=self.request.user.id)

        event_name = request.POST['event_name']
        event_date = request.POST['event_date']
        event_time = request.POST['event_time']
        location = request.POST['location']
        price = request.POST['price']
        total_tickets = request.POST['total_tickets']
        description = request.POST['description']
        event_image = request.FILES['event_image']

        se = AddEvent()

        se.organizer = user
        se.event_name = event_name
        se.event_date = event_date
        se.event_time = event_time
        se.location = location
        se.price = price
        se.total_tickets = total_tickets
        se.description = description
        se.event_image = event_image

        se.save()

        return HttpResponse("<script>alert('Event Added...');window.location='/organizer';</script>")

from django.utils import timezone

class viewevent(TemplateView):
    template_name = 'organizer/view_event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = OrganizerSignup.objects.get(user_id=self.request.user.id)
        events = AddEvent.objects.filter(organizer=user)

        context['event'] = events
        context['today'] = timezone.now().date()
        context['now'] = timezone.now().time()

        return context
class edit_event(TemplateView):
    template_name = "organizer/edit_event.html"

    def post(self, request, *args, **kwargs):

        event_id = request.POST.get('id')
        event = AddEvent.objects.get(id=event_id)

        if request.POST.get("event_name"):

            event.event_name = request.POST.get('event_name')
            event.event_date = request.POST.get('event_date')
            event.event_time = request.POST.get('event_time')
            event.location = request.POST.get('location')
            event.price = request.POST.get('price')
            event.total_tickets = request.POST.get('total_tickets')
            event.description = request.POST.get('description')

            if request.FILES.get('event_image'):
                event.event_image = request.FILES.get('event_image')

            event.save()

            return HttpResponse("<script>alert('Event Updated Successfully');window.location='/organizer/viewevent';</script>")

        return render(request, self.template_name, {'event': event})
    
class delete_event(View):
    def get(self, request, *args, **kwargs):
        event_id = request.GET.get('id')
        event = AddEvent.objects.get(id=event_id)
        event.delete()
        return HttpResponse("<script>alert('Event Deleted Successfully');window.location='/organizer/viewevent';</script>")

from django.views.generic import TemplateView
from django.db.models import Sum

from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import Sum
from .models import *



from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import Sum

class event_bookings(TemplateView):

    template_name = "organizer/view_bookings.html"

    def get(self, request, *args, **kwargs):

        organizer = OrganizerSignup.objects.get(user_id=request.user.id)

        # events created by organizer
        events = AddEvent.objects.filter(organizer=organizer)

        # all bookings
        bookings = Booking.objects.filter(event__in=events)

        # exclude cancelled bookings
        active_bookings = bookings.exclude(payment_status__iexact="cancelled")

        total_bookings = active_bookings.count()

        total_tickets = active_bookings.aggregate(
            total=Sum("quantity")
        )["total"] or 0

        total_revenue = active_bookings.aggregate(
            total=Sum("total_price")
        )["total"] or 0

        context = {
            "bookings": bookings,
            "total_bookings": total_bookings,
            "total_tickets": total_tickets,
            "total_revenue": total_revenue,
        }

        return render(request, self.template_name, context)
    
           
class organizer_feedback(TemplateView):
    template_name = "organizer/view_feedback.html"

    def get(self, request, *args, **kwargs):

        organizer = OrganizerSignup.objects.get(user_id=request.user.id)

        feedbacks = Feedback.objects.filter(event__organizer=organizer)

        context = {
            "feedbacks": feedbacks
        }

        return render(request, self.template_name, context)
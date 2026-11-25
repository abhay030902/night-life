from django.shortcuts import render
from django.views.generic import TemplateView,View
from django.contrib.auth.models import User
from nightlifeapp.models import *
from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import date, datetime
from django.db.models import Sum, Case, When, IntegerField

class adminhomeview(TemplateView):
    template_name="adminpage/index.html"

class organizerverify(TemplateView):
    template_name="adminpage/verify_organizer.html"
    
    def get_context_data(self, **kwargs):
        context = super(organizerverify,self).get_context_data(**kwargs)

        organizer = OrganizerSignup.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')

        context['organizer'] = organizer
        return context

class userverify(TemplateView):
    template_name="adminpage/verify_user.html"
    
    def get_context_data(self, **kwargs):
        context = super(userverify,self).get_context_data(**kwargs)

        user = UserSignup.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')

        context['user'] = user
        return context

class approve(View):
    def dispatch(self, request, *args, **kwargs):
 
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name='1'
        user.save()
        return HttpResponse(f"<script>alert(' Account Approved ');window.location.href='/adminpage/'</script>")          
    
class reject(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name='1'
        user.is_active='0'
        user.save()
        return HttpResponse(f"<script>alert(' Account Rejected ');window.location.href='/adminpage/'</script>")          

class viewuser(TemplateView):
    template_name="adminpage/view_user.html"
    
    def get_context_data(self, **kwargs):
        context = super(viewuser,self).get_context_data(**kwargs)

        user = UserSignup.objects.filter(user__last_name='1',user__is_staff='0',user__is_active='1')

        context['user'] = user
        return context
    
    
class vieworganizer(TemplateView):
    template_name="adminpage/view_organizer.html"
    
    def get_context_data(self, **kwargs):
        context = super(vieworganizer,self).get_context_data(**kwargs)

        organizer = OrganizerSignup.objects.filter(user__last_name='1',user__is_staff='0',user__is_active='1')

        context['organizer'] = organizer
        return context

class verify_event(TemplateView):
    template_name = "adminpage/verify_event.html"

    def get(self, request, *args, **kwargs):

        events = AddEvent.objects.all()

        context = {
            "event": events,
            "today": date.today(),
            "now": datetime.now().time()
        }

        return render(request, self.template_name, context)    
class approve_event(View):
    def dispatch(self, request, *args, **kwargs):
        id=request.GET['id']
        event=AddEvent.objects.get(id=id)
        event.status='approved'
        event.save()
        return HttpResponse(f"<script>alert('Event Approved ');window.location.href='/adminpage/'</script>")          
class reject_event(View):
    def dispatch(self, request, *args, **kwargs):
        id=request.GET['id']
        event=AddEvent.objects.get(id=id)
        event.status='rejected'
        event.save()
        return HttpResponse(f"<script>alert('Event Approved ');window.location.href='/adminpage/'</script>")          
       
class AdminReportView(TemplateView):

    template_name = "adminpage/view_report.html"

    def get(self, request, *args, **kwargs):

        events = AddEvent.objects.all()

        # ORDER BOOKINGS
        bookings = Booking.objects.annotate(
            order_status=Case(
                When(payment_status__iexact="cancelled", then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by("order_status", "-booking_date")

        # only booked for stats
        active_bookings = bookings.exclude(payment_status__iexact="cancelled")

        total_events = events.count()

        total_bookings = active_bookings.count()

        total_tickets = active_bookings.aggregate(
            Sum("quantity")
        )["quantity__sum"] or 0

        total_revenue = active_bookings.aggregate(
            Sum("total_price")
        )["total_price__sum"] or 0

        context = {
            "events": events,
            "bookings": bookings,
            "total_events": total_events,
            "total_bookings": total_bookings,
            "total_tickets": total_tickets,
            "total_revenue": total_revenue,
        }

        return render(request, self.template_name, context)
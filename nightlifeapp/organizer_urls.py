from django.urls import path
from nightlifeapp.organizer_views import *
 
urlpatterns=[
    path('',organizerhomeview.as_view(),name='organizer'),
    path('addevent',addevent.as_view(),name='addevent'),
    path('viewevent',viewevent.as_view(),name='viewevent'),
    path('edit_event',edit_event.as_view(),name='edit_event'),
    path('delete_event',delete_event.as_view(),name='delete_event'),
    path('viewbooking',event_bookings.as_view(),name='viewbooking'),
    path('organizer/feedback', organizer_feedback.as_view(), name='organizer_feedback'),
]
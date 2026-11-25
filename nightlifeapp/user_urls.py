from django import views
from django.urls import path
from flask import views
from nightlifeapp.user_views import *
 
urlpatterns=[
    path('',userhomeview.as_view(),name='user'),
    path('viewevent_user',viewevent.as_view(),name='viewevent_user'),
    path('viewmore_event',viewmore_event.as_view(),name='viewmore_event'),
    path('book_event', book_event.as_view(), name='book_event'),
    path('payment', payment.as_view(), name='payment'),
    path("ticket", mytickets.as_view(), name="ticket"),
    path("feedback", give_feedback.as_view(), name="feedback"),
    path("cancel_ticket",cancel_ticket.as_view(),name="cancel_ticket"),
]
from django.urls import path
from nightlifeapp.adminpage_views import *
 
urlpatterns=[
    path('',adminhomeview.as_view(),name='adminpage'),
    path('organizerverify',organizerverify.as_view(),name='organizerverify'),
    path('userverify',userverify.as_view(),name='userverify'),
    path('approve',approve.as_view()),
    path('reject',reject.as_view()),
    path('viewuser',viewuser.as_view(),name='viewuser'),
    path('vieworganizer',vieworganizer.as_view(),name='vieworganizer'),
    path('verify_event',verify_event.as_view(),name='verify_event'),
    path('approve_event',approve_event.as_view(),name='approve_event'),
    path('reject_event',reject_event.as_view(),name='reject_event'),
    path("admin/report/", AdminReportView.as_view(), name="admin_report"),

]
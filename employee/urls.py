from django.conf.urls import patterns, url
from employee import views

urlpatterns = patterns('',
   url(r'^handshake/$', views.Handshake.as_view()),
   url(r'^logout/$', views.LogOut.as_view()),
   url(r'^clockin/$', views.ClockIn.as_view()),
   url(r'^clockout/$', views.ClockOut.as_view()),
   url(r'^history/$', views.History.as_view()),
   url(r'^pay/$', views.Pay.as_view()),
   url(r'^loggedin/$', views.LoggedIn.as_view()),
)

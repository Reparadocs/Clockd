from django.conf.urls import patterns, url
from employer import views

urlpatterns = patterns('',
   url(r'^index/$', views.index, name='index'),
   url(r'^login/$', views.login, name='login'),
   url(r'^register/$', views.register, name='register'),
   url(r'^edit/(?P<employer_id>[0-9]+)/$', views.edit, name='edit'),
   url(r'^register_employee/$', views.register_employee, name='register_employee'),
   url(r'^edit_employee/(?P<employee_id>[0-9]+)/$', views.edit_employee, name='edit_employee'),
   url(r'^detail/(?P<employee_id>[0-9]+)/$', views.detail, name='detail'),
   url(r'^dashboard/(?P<employer_id>[0-9]+)/$', views.dashboard, name='dashboard'),
)

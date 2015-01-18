from django.db import models
from django.utils import timezone
from employer.models import Employer
import random
import datetime

def get_date_time(string):
   return datetime.datetime.strptime(string, "%d/%m/%Y")

class EmployeeManager(models.Manager):
   def create_employee(self, first_name, last_name, 
      employer, hourly_rate):
      
      while True:
         unique = random.randint(10000,99999)
         if not hasattr(employer, 'employee_set'): 
            break
         if employer.employee_set.count() == 0:
            break
         if not employer.employee_set.filter(unique=unique):
            break

      employee = self.create(first_name=first_name, 
         last_name = last_name,
         employer = employer,
         hourly_rate = hourly_rate,
         unique = unique)
      return employee

class Employee(models.Model):
   first_name = models.CharField(max_length=30)
   last_name = models.CharField(max_length=30)
   unique = models.IntegerField()
   hourly_rate = models.IntegerField()
   employer = models.ForeignKey(Employer)
   logged_in = models.BooleanField(default=False)

   objects = EmployeeManager()

   def __str__(self):
      return self.first_name + " " + self.last_name

   def login(self):
      self.save()

   def logout(self):
      self.save()

   def time_since_clockin(self):
      curentry = self.entry_set.filter(current=True)
      if curentry.count() is 1:
         current_entry = curentry[0]
         return (timezone.localtime(timezone.now()) - current_entry.time_in)
      else:
         return 0

   def str_time_since_clockin(self):
      td_sec = self.time_since_clockin().seconds
      hours = int(td_sec / 3600)
      minutes = int((hours % 3600) / 60)
      return str(hours) + " hours, " + str(minutes) + " minutes"

   def clockin(self):
      curentry = self.entry_set.filter(current=True)
      if curentry.count() is 0:
         self.logged_in = True
         entry = Entry(employee=self, time_in=timezone.localtime(timezone.now),
            time_1 = datetime.datetime.strftime("%m/%d/%Y %H:%M", timezone.localtime(timezone.now)))
         self.save()
         entry.save()
         return True
      else:
         return False

   def clockout(self):
      current_entry = self.entry_set.filter(current=True)
      if current_entry.count() is 1:
         self.logged_in = False
         current_entry.clockout(self.hourly_rate)
         return True
      else:
         return False

   def get_pay(self, datetime1, datetime2):
      history = self.get_history(datetime1, datetime2)
      total = 0
      for entry in history:
         total += entry.pay
      return total

   def get_approx_hours(self, datetime1, datetime2):
      dt_sec = (datetime2 - datetime1).sec
      return int(dt_sec/3600)

   def get_approx_hours_hist(self, datetime1, datetime2):
      history = self.get_history(datetime1, datetime2)
      total_hours = 0
      for entry in history:
         total_hours += get_approx_hours(entry.time_in, entry.time_out)
      return total_hours

   def get_overtime(self):
      shift_hours = int(time_since_clockin()/3600)
      period_start = timezone.localtime(timezone.now()) - datetime.timedelta(days=14)
      period_hours = get_approx_hours_hist(period_start, timezone.localtime(timezone.now()))
      if shift_hours < 8 and period_hours < 40:
         return "1x"
      elif shift_hours < 12 and period_hours < 55:
         return "1.5x"
      else:
         return "2x"

   def get_history(self, datetime1, datetime2):
      start = get_date_time(datetime1)
      end = get_date_time(datetime2)
      history = self.entry_set.filter(time_in__gte=start, 
         time_in__lte=end)
      return history


class Entry(models.Model):
   time_in = models.DateTimeField()
   time_1 = models.CharField(max_length=30)
   time_2 = models.CharField(max_length=30)
   current = models.BooleanField(default=True)
   time_out = models.DateTimeField(blank = True, null = True)
   employee = models.ForeignKey(Employee)
   pay = models.IntegerField(default=0)

   def clockout(self, rate):
      self.time_out = timezone.localtime(timezone.now())
      self.time_2 = datetime.datetime.strftime("%m/%d/%Y %H:%M", self.time_out)
      self.current = False
      seconds = (self.time_out - self.time_in).seconds
      self.pay = int(seconds * rate / 3600)
      self.save()

 


   

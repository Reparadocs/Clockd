from django.db import models
from django.utils import timezone
from employer.models import Employer
import random
import datetime

def get_date_time(arr):
   string = "%02d-%02d-%d"%(arr[1],arr[0],arr[2])
   return datetime.datetime.strptime(string, "%d-%m-%Y")

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
      self.logged_in = True
      self.save()

   def logout(self):
      self.logged_in = False
      self.save()

   def clockin(self):
      curentry = self.entry_set.filter(current=True)
      if curentry.count is 0:
         entry = Entry(employee=self, time_in=timezone.localtime(timezone.now()))
         self.save()
         entry.save()
         return True
      else:
         return False

   def clockout(self):
      current_entry = self.entry_set.filter(current=True)
      if(current_entry.count is 1):
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

   def get_history(self, datetime1, datetime2):
      start = get_date_time(datetime1)
      end = get_date_time(datetime2)
      history = self.entry_set.filter(time_in__gte=start, 
         time_in__lte=end)
      return history


class Entry(models.Model):
   time_in = models.DateTimeField()
   current = models.BooleanField(default=True)
   time_out = models.DateTimeField(blank = True, null = True)
   employee = models.ForeignKey(Employee)
   pay = models.IntegerField(default=0)

   def clockout(self, rate):
      self.time_out = timezone.localtime(timezone.now())
      self.current = False
      seconds = (self.time_out - self.time_in).seconds
      self.pay = int(seconds * rate / 3600)
      self.save()

 


   

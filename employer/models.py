from django.db import models
import random

class EmployerManager(models.Manager):
   def create_employer(self, name, ibeacon):
      while True:
         pin = random.randint(1000,9999)
         if not Employer.objects.filter(pin=pin):
            break

      employer = self.create(name=name, pin=pin, ibeacon=ibeacon)
      return employer

class Employer(models.Model):
   name = models.CharField(max_length=30)
   pin = models.IntegerField(unique=True)
   ibeacon = models.CharField(max_length=36)

   objects = EmployerManager()

   def __str__(self):
      return self.name

   def present_employees(self):
      employees = self.employee_set.filter(logged_in=True)
      return employees
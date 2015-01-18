from django import forms
from django.forms import ModelForm
from employer.models import Employer
from employee.models import Employee

class EmployerForm(ModelForm):
   class Meta:
      model = Employer
      fields = ['name','ibeacon']

class EmployeeForm(ModelForm):
   class Meta:
      model = Employee
      fields = ['first_name','last_name','hourly_rate']

class LoginForm(forms.Form):
   name = forms.CharField(label='Company Name', max_length=30)
   pin = forms.CharField(label='PIN',widget=forms.PasswordInput,max_length=4)
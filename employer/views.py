from django.shortcuts import render
from employer.forms import LoginForm, EmployerForm, EmployeeForm
from employer.models import Employer
from employee.models import Employee, Entry

def index(request):
   return render(request, 'index.html')

def login(request):
   if request.method == 'POST':
      form = LoginForm(data=request.POST)
      if form.is_valid():
         employer = Employer.objects.filter(name=form.cleaned_data['name'])
         if employer.count() is not 0:
            realemp = Employer.objects.filter(pin=form.cleaned_data['pin'])
            if realemp.count() is 1:
               real = realemp[0]
               return redirect(reverse('dashboard', args=(real.id)))
   else:
      form = LoginForm()
   return render(request, 'form.html', {'form': form})

def register(request):
   if request.method == 'POST':
      form = EmployerForm(request.POST)
      if form.is_valid():
         employer = Employer.objects.create_employer(name=form.cleaned_data['name'],
            ibeacon=form.cleaned_data['ibeacon'])
         employer.save()
         return redirect(reverse('dashboard', args=(employer.id)))
   else:
      form = EmployerForm()
   return render(request, 'form.html', {'form': form})

def edit(request, employer_id):
   employer = Employer.objects.get(pk=employer_id)
   if request.method == 'POST':
      form = EmployerForm(request.POST)
      if form.is_valid():
         employer.name = form.cleaned_data['name']
         employer.ibeacon = form.cleaned_data['ibeacon']
         employer.save()
         return redirect(reverse('dashboard', args=(employer_id)))
   else:
      form = EmployerForm(instance=employer)
   return render(request, 'form.html', {'form': form, 'employer': employer})

def register_employee(request, employer_id):
   employer = Employer.objects.get(pk=employer_id)
   if request.method == 'POST':
      form = EmployeeForm(request.POST)
      if form.is_valid():
         employee = Employee.objects.create_employee(first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'], employer=employer, 
            hourly_rate=form.cleaned_data['hourly_rate'])
         employee.save()
         return redirect(reverse('detail'), args=(employee.id))
   else:
      form = EmployeeForm()
   return render(request, 'form.html', {'form': form, 'employer': employer})

def edit_employee(request, employee_id):
   employee = Employee.objects.get(pk=employee_id)
   employer = employee.employer
   if request.method == 'POST':
      form = EmployeeForm(request.POST)
      if form.is_valid():
         employee.first_name = form.cleaned_data['first_name']
         employee.last_name = form.cleaned_data['last_name']
         employee.hourly_rate = form.cleaned_data['hourly_rate']
         employee.save()
         return redirect(reverse('detail'), args=(employee.id))
   else:
      form = EmployeeForm(instance=employee)
   return render(request,'form.html', {'form': form, 'employee': employee,
      'employer': employer})

def detail(request, employee_id):
   employee = Employee.objects.get(pk=employee_id)
   employer = employee.employer
   time_since = employee.str_time_since_clockin()
   return render(request, 'detail.html', {'employee':employee,'employer':employer,
      'time_since':time_since})

def dashboard(request, employer_id):
   employer = Employer.objects.get(pk=employer_id)
   cur_employees = employer.present_employees()
   return render(request, 'dashboard.html', 
      {'employer':employer,'cur_employees':cur_employees})


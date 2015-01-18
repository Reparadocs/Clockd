from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from employee.models import Employee, Entry
from employer.models import Employer
from employee.serializers import HandshakeSerializer, EntrySerializer, PaySerializer

def get_employee(pk):
   return Employee.objects.get(pk=pk)

class Handshake(APIView):
   def post(self, request, format=None):
      employer = Employer.objects.get(pin=request.data['pin'])
      if not employer:
         return HttpResponseBadRequest("Invalid Employer Pin")
      employee = employer.employee_set.get(unique=request.data['emp_id'])
      if not employee:
         return HttpResponseBadRequest("Invalid Employee ID")
      employee.login()
      serializer = HandshakeSerializer(employee, 
         context={'ibeacon': employer.ibeacon, 
            'employer_name': employer.name})
      return Response(serializer.data)

class LogOut(APIView):
   def post(self, request, format=None):
      employee = get_employee(request.data['employee_id'])
      if not employee:
         return HttpResponseBadRequest("Invalid Employee ID")
      employee.logout()
      return Response(status=status.HTTP_200_OK)

class ClockIn(APIView):
   def post(self, request, format=None):
      employee = get_employee(request.data['employee_id'])
      if not employee:
         return HttpResponseBadRequest("Invalid Employee ID")
      employee.clockin()
      return Response(status=status.HTTP_200_OK)

class ClockOut(APIView):
   def post(self, request, format=None):
      employee = get_employee(request.data['employee_id'])
      if not employee:
         return HttpResponseBadRequest("Invalid Employee ID")
      employee.clockout()      
      return Response(status=status.HTTP_200_OK)


class History(APIView):
   def post(self, request, format=None):
      employee = get_employee(request.data['employee_id'])
      if not employee:
         return HttpResponseBadRequest("Invalid Employee ID")
      history = employee.get_history(request.data['date1'], 
         request.data['date2'])
      return Response(EntrySerializer(history, many=True).data)

class Pay(APIView):
   def post(self, request, format=None):
      employee = get_employee(request.data['employee_id'])
      if not employee:
         return HttpResponseBadRequest("Invalid Employee ID")
      pay = employee.get_pay(request.data['date1'],
         request.data['date2'])
      return Response(PaySerializer(data={'pay':pay}).initial_data)

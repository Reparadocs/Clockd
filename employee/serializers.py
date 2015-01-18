from rest_framework import serializers
from employee.models import Employee, Entry

class EntrySerializer(serializers.ModelSerializer):
   class Meta:
      model = Entry
      fields = ('time_in','time_out')

class HandshakeSerializer(serializers.ModelSerializer):
   employer_name = serializers.SerializerMethodField('getEmployerName')
   ibeacon = serializers.SerializerMethodField('getIbeacon')

   def getEmployerName(self, obj):
      return self.context['employer_name']

   def getIbeacon(self, obj):
      return self.context['ibeacon']

   class Meta:
      model = Employee
      fields = ('id', 'first_name', 'last_name', 'hourly_rate',
       'employer_name', 'ibeacon')

class PaySerializer(serializers.Serializer):
   pay = serializers.IntegerField()
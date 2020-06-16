from django.contrib import admin
from firstapp.models import Doctor,Appointment,Patient,Person
# Register your models here.
#superuser/admin
#Jayanta
#jayantasadhu4557@gmail.com
#1234 password

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Person)
admin.site.register(Appointment)

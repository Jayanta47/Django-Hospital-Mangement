from django.db import models
#from django.urls import reverse
import datetime
import uuid
# Create your models here.

class Person(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    #id = models.IntegerField(primary_key = True, default =" " , unique= True)
    first_name =models.CharField(max_length = 50,default =" ")
    last_name = models.CharField(max_length = 50,default =" ")
    email = models.EmailField(max_length = 50, default = " ")
    address = models.CharField(max_length = 100,default = " ")
    phone = models.CharField(max_length=30,default = " ")
    gender = models.CharField(max_length = 6,default = " ")

    def __str__(self):
        return str(self.first_name+" "+self.last_name)
    def uniqueId(self):
        return str(self.id)

class Doctor(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    designation =models.CharField(max_length = 20,default = "DR.")
    edu = models.CharField(max_length = 20,default = "MBBS")
    join_date =models.DateField(("Date"), default=datetime.date.today)
    speciality = models.CharField(max_length=50,default =" ")
    Active = 'AC'
    Inactive = 'IC'
    STATUS = (
        (Active, 'Active'),
        (Inactive, 'Inactive')
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=Active,
    )

    def __str__(self):
        return self.person.first_name


class Patient(models.Model):
    person = models.OneToOneField(Person,on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.person.first_name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    Doctor = models.ForeignKey(Doctor , default=None,on_delete=models.CASCADE)
    Date = models.DateField(("Date"), default=datetime.date.today)
    Pending= 'PD'
    Approved= 'AP'
    Rejected = 'RJ'
    STATUS = (
        (Pending, 'Pending'),
        (Approved, 'Approved'),
        (Rejected, 'rejected'),
    )

    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=Pending,
    )

    message = models.CharField(max_length=1000 , default="Pending Approval")

    def __str__(self):
        return str(self.user)

from django.db import models

# Create your models here.
class Register_Form(models.Model):
    Name = models.CharField(max_length=25)
    Mobile = models.BigIntegerField()
    Email = models.EmailField()
    Password = models.BigIntegerField()
    

class Appointment_Booking(models.Model):
    Name = models.CharField(max_length=30)
    Email = models.EmailField()
    Mobile = models.BigIntegerField()
    Doctor = models.CharField(max_length=25)
    Date = models.DateField()
    Time =  models.TimeField()
    Detail = models.TextField()
    
class Contact_Form(models.Model):
    Name = models.CharField(max_length=30)
    Email = models.EmailField()
    Subject = models.CharField(max_length=350)
    Message = models.TextField()

class AdminSignUp(models.Model):
    UserName = models.CharField(max_length=250)
    Email = models.EmailField()
    Password = models.BigIntegerField()


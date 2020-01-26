from django.db import models

# Create your models here.
class Person(models.Model):
    p_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,blank=False)
    email = models.CharField(unique=True, max_length=255,blank=False)
    contact_number = models.CharField(unique=True,max_length=255)
    password = models.CharField(max_length=255,blank=False) 
    gender = models.CharField(max_length=255,blank=False)
    organization = models.CharField(max_length=255,blank=False)

class Request(models.Model):
    r_id = models.AutoField(primary_key=True)
    p_id = models.ForeignKey('Person', models.DO_NOTHING)
    seat_space = models.CharField(max_length=255,blank=False)
    c_location = models.CharField(max_length=255,blank=False)
    destination = models.CharField(max_length=255,blank=False)
    time = models.CharField(max_length=255,blank=False)
    message = models.CharField(max_length=255,blank=True)
    organization = models.CharField(max_length=255,blank=True)
    is_valid = models.CharField(max_length=1,blank=True,default='y')




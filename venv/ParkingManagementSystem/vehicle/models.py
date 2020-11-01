from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    categoryname = models.CharField(max_length=50)
    def __str__(self):
        return self.categoryname



class Vehicle(models.Model):
    parkingnumber = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vehiclecompany = models.CharField(max_length=50)
    regno = models.CharField(max_length=10)
    ownername = models.CharField(max_length=50)
    ownercontact = models.CharField(max_length=15)
    pdate = models.DateField()
    intime = models.CharField(max_length=50)
    outtime = models.CharField(max_length=50)
    parkingcharge = models.CharField(max_length=50)
    remark = models.CharField(max_length=500)
    status = models.CharField(max_length=20)
    def __str__(self):
        return self.parkingnumber




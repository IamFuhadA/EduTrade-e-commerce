from django.db import models

# Create your models here.

class RegistrationDB(models.Model):
    username=models.CharField(max_length=30,null=True,blank=True)
    name=models.CharField(max_length=30,null=True,blank=True)
    mail=models.EmailField(max_length=50,null=True,blank=True)
    contact=models.IntegerField(null=True,blank=True)
    password=models.CharField(max_length=30,null=True,blank=True)
    confirm_password=models.CharField(max_length=30,null=True,blank=True)
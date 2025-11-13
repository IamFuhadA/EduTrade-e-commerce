from django.db import models

# Create your models here.

class RegistrationDB(models.Model):
    username=models.CharField(max_length=30,null=True,blank=True)
    name=models.CharField(max_length=30,null=True,blank=True)
    mail=models.EmailField(max_length=50,null=True,blank=True)
    contact=models.IntegerField(null=True,blank=True)
    password=models.CharField(max_length=30,null=True,blank=True)
    confirm_password=models.CharField(max_length=30,null=True,blank=True)


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


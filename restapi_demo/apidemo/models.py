from django.db import models

# Create your models here.
class stock(models.Model):
    ticker=models.CharField(max_length=8)
    open = models.CharField(max_length=20)
    close = models.CharField(max_length=20)
    volume = models.CharField(max_length=100)


    def __str__(self):
        return self.ticker

class Registration(models.Model):
    firstname=models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20)

    def __str__(self):
        return self.firstname

class RestRegistration(models.Model):
    username=models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20,default='none')
    email=models.CharField(max_length=30)


    def __str__(self):
        return self.username

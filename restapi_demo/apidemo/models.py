from django.db import models
from django.core.validators import FileExtensionValidator

class RestRegistration(models.Model):       # Registration model for REST API.
    username=models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20,default='none')
    email=models.CharField(max_length=30)


    def __str__(self):
        return self.username


    def check_uname(self):
        return self.username



class Photo(models.Model):              # Model For profile picture
    file = models.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpeg'])])
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'



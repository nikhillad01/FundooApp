from django.contrib.auth.models import User
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

class Notes(models.Model):
    title = models.CharField(max_length=150,default=None)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    reminder = models.CharField(default=None, null=True,max_length=25)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    for_color = models.CharField(default=None, max_length=50, blank=True, null=True)
    image = models.ImageField(default=None, null=True)
    trash = models.BooleanField(default=False)
    is_pinned = models.NullBooleanField(blank=True, null=True, default=None)
    label = models.CharField(max_length=50,default=None,null=True)
    collaborate = models.ManyToManyField(User, null=True, blank=True, related_name='collaborated_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)

    def __str__(self):
        return self.title

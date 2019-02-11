from django.contrib.auth.models import User
from django.db import models

class RestRegistration(models.Model):
    username=models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20,default='none')
    email=models.CharField(max_length=30)


    def __str__(self):
        return self.username


    def check_uname(self):
        # if len(self.username)<20:
        #     return True
        return self.username


from django.db import models

class Photo(models.Model):
    file = models.ImageField()
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'


class Profile(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    # create image field
    image=models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
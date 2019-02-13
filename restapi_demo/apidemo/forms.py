from django.contrib.auth import get_user_model
from requests import request
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from PIL import Image
from django import forms
from .models import Photo
from .Upload_profile_pic_S3 import profile_pic
User= get_user_model()

class LoginForm(forms.ModelForm):
    model=User
    class Meta:
        fields=['username','password',]



class SignupForm(UserCreationForm):     # inheriting user-creation form to create form with following fields
    #email = forms.EmailField(max_length=200, help_text='Required')
    email=forms.RegexField(regex=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class loginForm(AuthenticationForm):     # inheriting user-creation form to create form with following fields
    #username = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username','password')

    def save(self, commit=True):
        user = super(loginForm, self).save(commit=False)
        #user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select a file')






class PhotoForm(forms.ModelForm):
    username = forms.CharField(required=True)
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())



    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )


    """X coordinate, Y coordinate, height and width of the cropping box """
    def save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        username = self.cleaned_data.get('username')
        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)
        #username=user.username
        #print(photo,'')
        #image.show()
        print('username thi ###########!!!!!!!!!!!!!@@@@@@@@@@@', username)
        path=photo.file.path
        profile_pic(request,path,username)
        #resized_image.save()
        return photo

        #return render(request,'photo_list.html',{resized_image})

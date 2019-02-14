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
    username = forms.CharField(required=True,label='Username',widget=forms.TextInput(attrs={'placeholder': 'Username '}))
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )


    """ X coordinate, Y coordinate, height and width of the cropping box """

    def save(self):
        username = self.cleaned_data.get('username')    # username to save image for particular user.

        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')      # X coordinate
        y = self.cleaned_data.get('y')      # X coordinate
        w = self.cleaned_data.get('width')  # width of cropping box
        h = self.cleaned_data.get('height')  # height of cropping box


        image = Image.open(photo.file)              # opens image file using Pillow library
        cropped_image = image.crop((x, y, w+x, h+y))        # crops image with x,y,w,h
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)  # resize cropped image.
        resized_image.save(photo.file.path)
        path=photo.file.path                    # gets the image path.
        profile_pic(request, path, username)      # calls method to upload pic to S3.

        return photo

    def clean_photo(self):
        #image_file = self.cleaned_data.get('photo')
        #super(PhotoForm, self)
        image_file = super(PhotoForm, self)
        if not image_file.name.endswith(".jpeg"):
            raise forms.ValidationError("Only .jpeg image accepted")
        return image_file
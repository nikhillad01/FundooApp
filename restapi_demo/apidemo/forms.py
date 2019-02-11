from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
User= get_user_model()

class LoginForm(forms.ModelForm):
    model=User
    class Meta:
        fields=['username','password',]


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

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






from PIL import Image
from django import forms
from django.core.files import File
from .models import Photo

class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('file', 'x', 'y', 'width', 'height', )

    def save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo
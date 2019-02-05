from django import forms
from django.contrib.auth import get_user_model

from  .models import Registration
User= get_user_model()
class Registrationform(forms.ModelForm):
    class Meta:
        model= Registration
        fields =[
            'firstname',
            'lastname',
            'email',
            'password',
            'confirm_password',
        ]

class LoginForm(forms.ModelForm):
    model=User
    class Meta:
        fields=['username','password',]


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class SignupForm(UserCreationForm):     # inheriting user-creation form to create form with following fields
    email = forms.EmailField(max_length=200, help_text='Required')

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
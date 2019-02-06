from django.contrib import messages, auth
from django.http import HttpResponse, HttpRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.backends import django
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, authenticate
import jwt,json
from rest_framework.response import Response
from .serializers import TokenAuthentication
from .serializers import registrationSerializer
from rest_framework.generics import CreateAPIView

from jinja2 import Environment,PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('apidemo', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def index(request):         # this is homepage.
    return render(request, 'index.html', {})
def login_u(request):
    return  render(request,'login.html',{})
def login_without(request):
    return  render(request,'rest_framework/vertical.html',{})
def dash(request):      # /dash/
    return render(request,'dashboard.html',{})


User= get_user_model()          # will retrieve the USER model class.
import re

class UserCreateAPI(CreateAPIView):             # Registration using Rest framework Using User Model.

    serializer_class=registrationSerializer
    queryset = User.objects.all()                  # fields according to User   (adds data to USER model)

class LoginView(APIView):
    #hasher = PBKDF2PasswordHasher()

    serializer_class = TokenAuthentication
    queryset = User.objects.all()
    http_method_names = ['post', 'get']      # to use POST method by default it was using GET.


    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            print(user,'this is userrrrrrr')
            if user:
                if user.is_active:
                    #login(user)
                    payload = {'username': username,
                                'password': password,}


                    jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256')}
                                                                            # generates the token using payload information.

                            #template = env.get_template('dashboard.html')   # using Jinja2 to get the dashboard template

                    #template.render(username=username)             # renders to template with variable username.

                    #return render_template()
                    return HttpResponse(
                     #jwt_token,
                    #user.username,
                     jwt_token.values(),
                        #json.dumps(list(jwt_token['token'])),
                        #json.dumps(jwt.decode(jwt_token)),
                        status=200,
                        content_type="application/json"
                    )
                    #return HttpResponseRedirect(reverse('rest_register'))
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                    print("Someone tried to login and failed.")
                    print("They used username: {} and password: {}".format(username, password))
                    return HttpResponse("Invalid login details given")

        else:
            return render(request, 'dashboard.html', {})
    ############################





def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False      # user disabled
            user.save()                 # stores in database.
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain':'http://127.0.0.1:8000',
                #'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),  # coz django 2.0.0
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your Fundoo account.'  # mail subject
            to_email = form.cleaned_data.get('email')       # mail id to be sent to
            email = EmailMessage(mail_subject, message, to=[to_email])   # takes 3 args: 1. mail subject 2. message 3. mail id to send
            email.send()        # sends the mail
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print('Uid:             :',uid)
        user = User.objects.get(pk=uid)     # gets the username
        print('user:::::',user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponsePermanentRedirect(reverse('rest_login'))
    else:
        return HttpResponse('Activation link is invalid!')

def login_v(request):
    return render(request, 'login.html')


from django.http import Http404
def demo_user_login(request):

    if request.method=="POST":
        username=request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        try:
            user = authenticate(username=username, password=password)
        except user.DoesNotExist:
            raise Http404("No Such Data found.")
        login(request,user)
        try:
            if user:
                   if user.is_active:
                        payload = {'username': username,
                                      'password': password}


                        jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256')}
                                                                                # generates the token using payload information.
                        messages.success(request,username)
                        return render(request, 'dashboard.html', {})
                        # return HttpResponse(
                        #  jwt_token.values(),
                        #     #json.dumps(list(jwt_token['token'])),
                        #     #json.dumps(jwt.decode(jwt_token)),
                        #     status=200,
                        #     content_type="application/json"
                        # )
                        #return HttpResponseRedirect(reverse('rest_register'))
                   else:
                        msg="Your account was inactive."
                        return HttpResponse(messages.error(request,msg))
        except Exception as e: print(e)
        else:
                     msg="Invalid login details given"
                     #return HttpResponse(messages.error(request,'Invalid login credentials'))
                     messages.error(request, 'Invalid login details')
                     return render(request, 'login.html')

    else:
        return render(request, 'login.html', {})

def open_upload_form(request):
    return render(request,'fileupload.html',{})


import boto3

def upload_profile(request):
    #return HttpResponse("uploaded successfully")
    if request.method=='POST':
        print()
        #uname=request.POST.get['username']
        print('******************** in Upload view*********************')
        print()
        s3 = boto3.client('s3')
        try:
            print('***************** boto 3 ***********************')
            file = request.FILES['pic']
            username=request.POST.get('username')
            print('*******************',username)
            print('******************** In FILESSSS*********************')
            key=username+'.jpeg'
            print('this is keyyyyyyyyyyyyyyyyyyyyyyyyyy',key)
            #s3.upload_file(file,'fundoo','test1.jpeg')
            s3.upload_fileobj(file, 'fundoo', Key=key)
        except MultiValueDictKeyError:
            messages.error(request, "Please select valid file")
            return render(request, 'profile.html')
            #return HttpResponse("Please select valid file")
        return render(request,'dashboard.html')
    else : return HttpResponse("GET Request")

def profile_page(request):
    return render(request,'profile.html',{})

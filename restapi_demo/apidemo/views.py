from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth import login
from .forms import SignupForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, authenticate
import jwt
from .serializers import TokenAuthentication
from .serializers import registrationSerializer
from rest_framework.generics import CreateAPIView
from .Upload_profile_pic_S3 import profile_pic
from .forms import PhotoForm
from django.contrib.sites.models import Site
from django.shortcuts import render, redirect

def index(request):         # this is homepage.1
    return render(request, 'index.html', {})

def login_u(request):
    return render(request, 'login.html',{})

def login_without(request):
    return render(request, 'rest_framework/vertical.html',{})

def dash(request):      # /dash/
    return render(request, 'dashboard.html',{})

def profile_page(request):
    return render(request, 'profile.html', {})

def logout(request):
    auth.logout(request)
    return render(request, 'login.html')

def base(request):
    return render(request, 'in.html')


User= get_user_model()          # will retrieve the USER model class.

class UserCreateAPI(CreateAPIView):             # Registration using Rest framework Using User Model.

    serializer_class=registrationSerializer
    queryset = User.objects.all()                  # fields according to User   (adds data to USER model)

class LoginView(APIView):

    serializer_class = TokenAuthentication
    queryset = User.objects.all()
    http_method_names = ['post', 'get']      # to use POST method by default it was using GET.

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    payload = {'username': username,        # creates token using Payload.
                                'password': password, }
                    jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256')}
                    return HttpResponse(        # returns token as response with success status code.
                     jwt_token.values(),
                        status=200,
                        content_type="application/json"
                    )
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                    print("Someone tried to login and failed.")
                    print("They used username: {} and password: {}".format(username, password))
                    return HttpResponse("Invalid login details given")
        else:
            return render(request, 'dashboard.html', {})




def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # object  hasn't yet been saved to the database.
            user.is_active = False          # user disabled
            user.save()                     # stores in database.
            data = {                        # renders to html with variables
                #"urlsafe_base64_encode" takes user id and generates the base64 code(uidb64).
                'user': user,
                'domain':'http://127.0.0.1:8000',
                #'uid': urlsafe_base64_encode(force_bytes(user.pk)),    # encodes
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),  # coz django 2.0.0 to convert it to string
                'token': account_activation_token.make_token(user),  # creates a token
            }
            message = render_to_string('acc_active_email.html', data)
            mail_subject = 'Activate your Fundoo account.'  # mail subject
            to_email = form.cleaned_data.get('email')       # mail id to be sent to
            email = EmailMessage(mail_subject, message, to=[to_email])   # takes 3 args: 1. mail subject 2. message 3. mail id to send
            email.send()        # sends the mail
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})       # if  GET request



def activate(request, uidb64, token):

    """  This method is used to activate the user when clicks the email link """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))         # decode to string find the primary key of user
        user = User.objects.get(pk=uid)     # gets the username
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True           # enables the user
        user.save()                     # saves to DB.
        return HttpResponsePermanentRedirect(reverse('login_v'))
    else:
        return HttpResponse('Activation link is invalid!')

def login_v(request):               # renders to login page.
    return render(request, 'login.html')



@require_POST
def demo_user_login(request):

    """ This method is used to log in user """

    username = request.POST.get('username')             # takes the username from request
    password = request.POST.get('password')             # takes password from request .
    print(username, password)
    user = authenticate(username=username, password=password)       # checks if username and password are available in DB.
    if user:
        if user.is_active:
            login(request, user)
            payload = {'username': username,
                       'password': password}
            jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256').decode()}    # creates the token using payload String Token
            j = jwt_token['token']
            messages.success(request, username)
            return render(request, 'in.html', {'token': j})   # renders to page with context=token
        else:
            msg = "Your account was inactive."
            return HttpResponse(messages.error(request, msg))
    else:
        messages.error(request, 'Invalid login details')
        return render(request, 'login.html')


def open_upload_form(request):
    return render(request, 'fileupload.html', {})


@require_POST
@login_required
def upload_profile(request):

    """ This method is used to upload a profile picture to S3 bucket """

    #profile_pic(request)                      # calls profile_pic upload method from S3 Upload file.
    messages.success(request, "Profile Pic updated")    # returns success message
    return render(request, 'profile.html')

def crop(request):
    return render(request,'photo_list.html')


def photo_list(request):

    """This method is used to upload a profile picture with cropping functionality"""

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)           # django form
        if form.is_valid():
            form.save()  # Saves the form.
            return redirect('photo_list')
    else:
        form = PhotoForm()                  # renders to page with form
        return render(request, 'photo_list.html', {'form': form})
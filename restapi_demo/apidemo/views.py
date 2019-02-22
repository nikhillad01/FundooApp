from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth import login
from .models import Notes
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
from .forms import PhotoForm
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.core.paginator import Paginator
from .serializers import NoteSerializer
from rest_framework import status, generics

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
@permission_classes([AllowAny, ])
def demo_user_login(request):

    res = {
        'message': 'Something bad happened',
        'data': {},
        'success': False
    }

    """ This method is used to log in user """

    try:
        username = request.POST.get('username')             # takes the username from request
        password = request.POST.get('password')             # takes password from request .
        if username is None:
            raise Exception('Username is required')
        if password is None:
            raise Exception('Password is required')
        print(username, password)
        user = authenticate(username=username, password=password)       # checks if username and password are available in DB.
        if user:
            if user.is_active:
                login(request, user)
                payload = {'username': username,
                           'password': password}
                jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256').decode()}    # creates the token using payload String Token
                j = jwt_token['token']
                #messages.success(request, username)
                res['message']="Logged in Successfully"
                res['success']=True
                cache.set('token', "token")
                res['data'] =j
                print(res)
                return render(request, 'in.html', {'token':res})   # renders to page with context=token
                #return HttpResponseRedirect(reverse('getnotes'),content={"token":res})
            else:
                res['message'] = "Your account was inactive."
                return render(request, 'in.html', res)

        else:
            res['message'] = 'Username or Password is not correct' #Invalid login details
            messages.error(request, 'Invalid login details')
            return render(request, 'login.html', context=res)
    except Exception as e:
        print(e)
        return render(request, 'login.html', context=res)


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


def demo(request):
    return render(request,'demo.html',{})




# API to create note

class AddNote(CreateAPIView):

    serializer_class=NoteSerializer     # serializer to add note(specifies and validate )

    def post(self, request):
        try:
            #print(request.data)
            #print(request.data['remainder'])

            res = {                                 # Response information .
                'message': 'Something bad happened',
                'data': {},
                'success': False
            }

            print('user--->',request.data['user'])
            print(request.data)
            print('for color',request.data['for_color'])
            serializer = NoteSerializer(data=request.data)
            # check serialized data is valid or not

            if request.data['title'] and request.data['description'] is None:   # if title and description is not provided.
                raise Exception("Please add some information ")

            if serializer.is_valid():
                                            # if valid then save it
                serializer.save()
                                            # in response return data in json format
                return HttpResponseRedirect(reverse('getnotes'),content=res)

                                            # else return error msg in response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return redirect(reverse('getnotes'))



class getnotes(View):

    def get(self, request):

        """ This method is used to read all notes """

        res = {
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        """This method is used to read all the notes from database."""

        try:
            #note_list = Notes.objects.all().order_by('-created_time')       # gets all the note and sort by created time
            note_list = Notes.objects.filter(user=request.user).order_by('-created_time')   # shows note only added by specific user.
        except Exception as e:
            print(e)

        paginator = Paginator(note_list, 9)          # Show 9 contacts per page
        page = request.GET.get('page')
        notelist = paginator.get_page(page)

        res['message'] = "All Notes"
        res['success'] = True
        res['data'] =notelist

        return render(request, 'in.html', {'notelist': notelist})



class updatenote(CreateAPIView):
    serializer_class = NoteSerializer
    def put(self, request, pk):
        serializer = NoteSerializer(data=request.data)
        """This method is used to update the notes"""

        res = {
            'message': 'Something bad happened',    # response information
            'data': {},
            'success': False
        }

        if pk is None:                          # checks if primary key is passed
            raise ValueError

        if request.data is None:                # checks data is present in request
            raise Exception('No data in request')

        try:
            note = Notes.objects.get(pk=pk)     # checks if primary key is available in DB and gets the data
        except Exception as e:
            print(e)
            return JsonResponse(res)

       # serializer = NoteSerializer(note, data=request.data)  # check serialized data is valid or not

        if serializer.is_valid():
            # if valid then save it
            serializer.save()
            # in response return data in json format
            res = {
                'message': 'Updated Successfully',
                'data': serializer.data,
                'success': True
            }
            return Response(res, status=status.HTTP_201_CREATED)
        # else return error msg in response
        return Response(res, status=status.HTTP_400_BAD_REQUEST)



def deleteN(request,id):

    """This method is used to delete the note"""

    res = {
        'message': 'ID not found',  # response information
        'data': {},
        'success': False
    }

    if id is None:                              # check is ID is not None
                                                #raise Exception('ID not found')
        return JsonResponse(res)
    else:
        try:
            item = Notes.objects.get(pk=id)     # checks if note is present of specific id
        except Exception as e:
            print(e)
            res['message']="Note not present for specific ID"
            return JsonResponse(res)

        item.delete()
        return redirect(reverse('getnotes'))


def updateform(request,pk):
        note = Notes.objects.get(id=pk)
        return render(request,'Notes/update.html',{"note":note})

def updateNotes(request,pk):
    note=Notes.objects.get(id=pk)
    print(note)
    title=request.POST.get('title')
    description = request.POST.get('description')
    ctime = request.POST.get('ctime')
    remainder = request.POST.get('remainder')
    colla = request.POST.get('colla')
    print(title,colla,description)
    note.title=title
    note.description=description
    note.created_time=ctime
    note.remainder=remainder
    note.collaborate=colla
    note.save()
    print(note)
    return HttpResponse('up[dated')
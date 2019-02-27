from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views import View
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
from rest_framework.generics import CreateAPIView, UpdateAPIView
from .forms import PhotoForm
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.core.paginator import Paginator
from .serializers import NoteSerializer
from rest_framework import status
from .custom_decorators import custom_login_required

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
#@login_required
class AddNote(CreateAPIView):   # CreateAPIView used for create only operations.

    """This class is used to create a note with REST """

    serializer_class=NoteSerializer     # serializer to add note(specifies and validate )

    def post(self, request):

        try:

            res = {                                 # Response information .
                'message': 'Something bad happened',
                'data': {},
                'success': False
            }

            serializer = NoteSerializer(data=request.data)  # takes the data from form.
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
            return redirect(reverse('getnotes'))        # redirects to getnotes view



class getnotes(View):

    def get(self, request):
        # print(request.META)
        for  i in request.META:
            print(i)

       # print('Authorization',authorization)
        """ This method is used to read all notes """

        res = {
            'message': 'Something bad happened',    # Response Data
            'data': {},
            'success': False
        }

        """This method is used to read all the notes from database."""
        print('request user',request.user)
        try:
            #note_list = Notes.objects.all().order_by('-created_time')   # gets all the note and sort by created time
            note_list = Notes.objects.filter(user=request.user,trash=False,is_archived=False).order_by('-created_time')   # shows note only added by specific user.

            labels = Labels.objects.filter(user=request.user).order_by('-created_time')
            print(labels)
            paginator = Paginator(note_list, 9)          # Show 9 contacts per page
            page = request.GET.get('page')
            notelist = paginator.get_page(page)

            res['message'] = "All Notes"
            res['success'] = True
            res['data'] =notelist

            return render(request, 'in.html', {'notelist': notelist,'labels':labels})

        except Exception as e:
            print(e)


class updatenote(UpdateAPIView):


    """Updates notes  using REST Framework"""

    serializer_class = NoteSerializer       # Serializer

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


@custom_login_required
def deleteN(request,id):

    """This method is used to delete the note
    pk: Primary key
    """

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
        item.trash=True
        item.save()
        return redirect(reverse('getnotes'))

@custom_login_required
def updateform(request,pk):

    # this method is used to open the update note form for particular note

    res = {
        'message': 'ID not found',  # response information
        'data': {},
        'success': False
    }

    if pk ==None:                      # if Pk is not provided.
        raise Exception('Invalid Details')

    try:
        note = Notes.objects.get(id=pk)  # gets the note with  PK

    except Exception as e:
        return HttpResponse(e)

    return render(request, 'Notes/update.html', {"note": note})





@custom_login_required
def updateNotes(request,pk):

    """ This method is used to update the notes
    pk: Primary key
    """
    pk_note=request.POST.get('pk_note')
    print('found pk',pk_note)
    pk=pk_note
    res = {
        'message': 'ID not found',  # response information
        'data': {},
        'success': False
    }

    if pk is None:                  # if pk is not provided.
        raise Exception('Invalid Details')
    print("if dwn")
    title=request.POST.get('title')
    update_description=request.POST.get('description')
    print(title)
    print(update_description)
    try:

        note=Notes.objects.get(id=pk_note)       # gets the data with primary key
        print('note',note)

        # if request.POST['update_title']==None:             # if title is None.
        #     raise Exception('No Valid details provided')

        title=request.POST.get('title')
        description = request.POST.get('description')
        # ctime = request.POST.get('ctime')
        # remainder = request.POST.get('remainder')
        # colla = request.POST.get('colla')

                              # changing data of note with form data.

        note.title=title
        note.description=description
        # note.created_time=ctime
        # note.remainder=remainder
        #note.collaborate=colla
        note.save()             # saves the updated data
    except Exception as e:
        print('exception')
        print(e)
    return redirect(reverse('getnotes'))



@custom_login_required
def pin_unpin(request,pk):

    """This method is used to make note pinned or unpinned
     pk: Primary key
     """

    if pk==None:                # if Pk is not provided
        raise Exception('invalid Details')

    try:
        item = Notes.objects.get(id=pk)         # gets particular item from DB with PK.
    except Exception as e:
        return HttpResponse("Note not found")

    if item.is_pinned == False or item.is_pinned==None:
        item.is_pinned=True         # if item is not pinned or False .. pin it
        item.save()                 # saves to the DB.
        messages.success(request,message='Note pinned')
        return redirect(reverse('getnotes'))
    else:
        item.is_pinned=False            # if item is already pinned , unpin it.
        item.save()
        messages.success(request,message='Note Unpinned')
        return redirect(reverse('getnotes'))


@custom_login_required
def trash(request,pk):
    """This method is used to push item to trash
    pk: Primary key
    """
    if pk == None:                  # if Pk is Not provided.
        raise Exception('Invalid details')

    try:
        item=Notes.objects.get(id=pk)
    except Exception as e :
        return HttpResponse("No item found ")


    if item.trash==False or item.trash==None:
        item.trash=True         # if trash field is None or False, make note trash
        item.save()
        messages.success(request, message='Item moved to trash')
        return redirect(reverse('getnotes'))
    elif item.trash==True:          # if item already in trash restore it.
        item.trash=False
        item.save()
        messages.success(request,message='item restored')



class view_trash(View):

    """This method is used to display all the items which are in trash"""

    def get(self, request):


        res = {
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        """ gets all the  notes which are added by specific user and which are in Trash """

        try:
            note_list = Notes.objects.filter(user=request.user, trash=True).order_by('-created_time')  # shows note only added by specific user.
        except Exception as e:
            print(e)

        paginator = Paginator(note_list, 9)  # Show 9 contacts per page
        page = request.GET.get('page')        # also used as prefix in URL
        notelist = paginator.get_page(page)     # gets data page by page

        res['message'] = "All Trash Notes"
        res['success'] = True
        res['data'] = notelist
        print(notelist)
        return render(request, 'in.html', {'notelist': note_list})

@custom_login_required
def delete_forever(request, pk):

    """This method is used to permanently delete the note
    pk: Primary key
    """
    if pk is None:
        raise Exception("Invalid details")

    try:
        item = Notes.objects.get(id=pk)
    except Exception as e :
        return HttpResponse("Note not found ")

    item.delete()       # deletes the note permanently
    messages.success(request, message='Item Deleted forever')
    return redirect(reverse('getnotes'))

@custom_login_required
def is_archived(request,pk):

    """This method is used to make note archive
    pk: Primary key
    """

    if pk==None:            # if Pk is not provided.
        raise Exception("invalid details")
    try:
        item = Notes.objects.get(id=pk)
    except Exception as e:
        return  HttpResponse("Note not found")

    if item.is_archived == False or item.is_archived == None:      # if archive field is false or None.
        item.is_archived = True                 # make note archive
        item.save()
        messages.success(request, message='Item is archived')
        return redirect(reverse('getnotes'))
    elif item.is_archived == True:          # it item is already archived
        item.is_archived = False
        item.save()
        messages.success(request, message='Removed from archived')
        return redirect(reverse('getnotes'))



class View_is_archived(View):

    """This method is used to display all the notes which are archived

    """

    def get(self, request):

        """ Reads the notes by user and archived field"""

        res = {
            'message': 'Something bad happened',
            'data': {},
            'success': False
        }

        """This method is used to read all the notes from database."""

        try:
                  # gets all the note and sort by created time
            note_list = Notes.objects.filter(user=request.user, is_archived=True).order_by('-created_time')  # shows note only added by specific user.
        except Exception as e:
            print(e)

        paginator = Paginator(note_list, 9)  # Show 9 contacts per page
        page = request.GET.get('page')
        notelist = paginator.get_page(page)

        res['message'] = "All Trash Notes"
        res['success'] = True
        res['data'] = notelist
        print(note_list)
        return render(request, 'in.html', {'notelist': note_list})

from .models import Labels,Map_labels
def add_labels(request,pk):
    label_name=request.POST['label_name']
    user=pk

    label=Labels.objects.create(user=User.objects.get(id=user),label_name=label_name)
    label.save()
    messages.success(request, message='Label Created')
    return redirect(reverse('getnotes'))

def map_labels(request):
    label_id=request.POST['label_id']
    user=request.POST['user']
    note=request.POST['note']

    map=Map_labels.objects.create(label_id=Labels.objects.get(id=label_id),user=User.objects.get(id=user),note=Notes.objects.get(id=note))
    map.save()
    return HttpResponse("Label mapped")

def delete_label(request,pk):
    label=Labels.objects.get(id=pk)
    label.delete()
    messages.success(request, message='Label deleted')
    return redirect(reverse('getnotes'))


def view_notes_for_each_label(request):

    label_id=request.POST['label_id']
    user_id=request.POST['user_id']
    print(label_id)
    print(user_id)

    note_list = Map_labels.objects.filter(user_id=user_id,label_id=label_id)
    # messages.success(request, message='Label deleted')
    # return redirect(reverse('getnotes'))
    print(note_list)
    return HttpResponse(note_list)
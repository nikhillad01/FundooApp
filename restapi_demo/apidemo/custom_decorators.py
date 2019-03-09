from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from .redis_info import r
import jwt

def custom_login_required(function=None,login_url =''):
    try:
        def is_login(u):
            token = r.get('token')  # gets the token from redis cache
            token = token.decode(encoding='utf-8')  # decodes the token ( from Bytes to str )
            decoded_token = jwt.decode(token, 'secret_key',
                                       algorithms=['HS256'])  # decodes JWT token and gets the values Username etc
            user = User.objects.get(username=decoded_token['username']).pk  # gets the user from username
            return User.objects.filter(pk=user).exists()     # if user is present in DB.
        actual_decorator = user_passes_test(is_login)           # user_passes_test to check if some test passes or not
        if function:
            return actual_decorator(function)
        else:
            return redirect(reverse('login_v'))
            #return actual_decorator

    except (ObjectDoesNotExist,Exception) as e:
        print(e)
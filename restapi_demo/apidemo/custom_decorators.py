from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse


def custom_login_required(function=None,login_url =''):
    try:
        def is_login(u):
            print('this is user',u)
            return User.objects.filter(username=u).exists()
        actual_decorator = user_passes_test(is_login)
        if function:
            return actual_decorator(function)
        else:
            return redirect(reverse('login_v'))
            #return actual_decorator

    except (ObjectDoesNotExist,Exception) as e:
        print(e)
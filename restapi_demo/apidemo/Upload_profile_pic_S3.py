import boto3
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError


def profile_pic(request):
    s3 = boto3.client('s3')  # creates S3 connection
    file = request.FILES['pic']
    try:

        username = request.POST.get('username')
        key = username + '.jpeg'
        s3.upload_fileobj(file, 'fundoo', Key=key)
        messages.error(request, "Profile Pic updated")
        return render(request,'profile.html')
    except (MultiValueDictKeyError,Exception):  # handles error if no file is selected while submitting
        messages.error(request, "Please select valid file")
        return render(request, 'profile.html')
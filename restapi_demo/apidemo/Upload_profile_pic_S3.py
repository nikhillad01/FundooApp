import boto3
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse

def profile_pic(request,path,username):
        s3 = boto3.client('s3')  # creates S3 connection
        file=open(path,'rb')

        try:
            key = username + '.jpeg'
            s3.upload_fileobj(file, 'fundoo', Key=key)
            #messages.error(request, "Profile Pic updated")
            #return render(new_request,'profile.html')
            return HttpResponse("Profile Photo Updated successfully")
        except (MultiValueDictKeyError,Exception):  # handles error if no file is selected while submitting
            #messages.error(request, "Please select valid file")
            return render(request, 'profile.html')
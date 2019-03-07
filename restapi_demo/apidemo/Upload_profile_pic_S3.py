import boto3
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse

"""This method is used to upload a cropped image to S3 bucket"""

def profile_pic(request, path, username):

        s3 = boto3.client('s3')  # creates S3 connection
        file=open(path, 'rb')   # image to upload with read access

        key = username +'.jpeg'

        try:
                    # image name  in S3
            s3.upload_fileobj(file, 'fundoo', Key=key)
            return HttpResponse("Profile Photo Updated successfully")
        except (MultiValueDictKeyError,Exception):  # handles error if no file is selected while submitting
            return HttpResponse("Not valid")
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from . import services

"""This method is used to upload a cropped image to S3 bucket"""

def profile_pic(request, path, username):


        file=open(path, 'rb')   # image to upload with read access

        key = username +'.jpeg'

        try:
                    # image name  in S3
            services.s3.upload_fileobj(file, 'fundoo', Key=key)
            return HttpResponse("Profile Photo Updated successfully")
        except (MultiValueDictKeyError,Exception):  # handles error if no file is selected while submitting
            return HttpResponse("Not valid")
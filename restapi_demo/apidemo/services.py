"""This file contains details about services required
    i.e. Cloud and Redis
"""

import boto3
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
import redis
import imghdr



s3 = boto3.client('s3')                                    # connection for S3.
r = redis.StrictRedis(host='localhost', port=6379, db=0)   # Redis connection

def upload_image(request, path, username):

    """This method is used to upload the images to Amazon s3 bucket"""

    file = open(path, 'rb')  # image to upload with read access
    key = username           # image name  in S3
    try:

        s3.upload_fileobj(file, 'fundoo', Key=key)
        return HttpResponse("Profile Photo Updated successfully")
    except (MultiValueDictKeyError, Exception):  # handles error if no file is selected while submitting
        return HttpResponse("Not valid")



class redis_info:

    """This class is used to set , get and delete data from Redis cache
            StrictRedis does not provide compatibility for older versions of redis.py
            Do you need backwards compatibility ? Use Redis
    """

    try:
        def set_token(self, key, value):
             if key and value:          # adds the data to redis
                r.set(key, value)


        def get_token(self, key):

             if key:                    # gets the data out of redis
                value=r.get(key)
                return value


        def flush_all(self):
            r.flushall(asynchronous=False)          # deletes all data from redis cache

    except Exception as e:
        print(e)
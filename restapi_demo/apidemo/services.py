"""
* Purpose:This file contains details about services required
          i.e. Cloud and Redis
* @author: Nikhil Lad
* @version: 3.7
* @since: 10-3-2019
"""

import boto3
from django.http import HttpResponse, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
import redis

s3 = boto3.client('s3')                                    # connection for S3.
r = redis.StrictRedis(host='localhost', port=6379, db=0)   # Redis connection

def upload_image(request, path, username):

    """This method is used to upload the images to Amazon s3 bucket"""

    if path and username:

        file = open(path, 'rb')  # image to upload with read access

        try:
            s3.upload_fileobj(file, 'fundoo', Key=username)
            return HttpResponse("image uploaded successfully")
        except (MultiValueDictKeyError, Exception):  # handles error if no file is selected while submitting
            return HttpResponse("Not valid")
    else:
        return HttpResponse("something bad happened")



def delete_object_from_s3(request,key):

    """This method is used to delete any object from s3 bucket """
    res = {
        'message': 'Something Bad Happened',  # Response Data
        'data': {},
        'success': False
    }

    try:
        if key:
            s3.delete_object(Bucket='fundoo', Key=key)
            res['message']="successfully deleted"
            res['success']=True
            return JsonResponse(res)
        else:
             return JsonResponse(res)
    except (MultiValueDictKeyError,KeyboardInterrupt,ValueError,Exception) as e:
        print('exception')



class redis_info:

    """This class is used to set , get and delete data from Redis cache
            StrictRedis does not provide compatibility for older versions of redis.py
            Do you need backwards compatibility ? Use Redis
    """
    res = {
        'message': 'Something Bad Happened',  # Response Data
        'data': {},
        'success': False
    }

    try:
        def set_token(self, key, value):
             if key and value:                     # adds the data to redis
                r.set(key, value)

             else:
                return JsonResponse({'message': 'Invalid detail provided'})


        def get_token(self, key):

             if key:                               # gets the data out of redis
                value=r.get(key)
                return value
             else:
                 return JsonResponse({'message':'Invalid detail provided'})


        def flush_all(self):
            try:
                r.flushall(asynchronous=False)         # deletes all data from redis cache
            except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception):
                return JsonResponse({"message": "Something bad happened"})
    except (KeyboardInterrupt, MultiValueDictKeyError, ValueError, Exception) as e:
        print(e)


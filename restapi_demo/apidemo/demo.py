# import boto3
#
# s3 = boto3.resource('s3')
# my_bucket = s3.Bucket('fundoo')
#
# for object_summary in my_bucket.objects.filter():
#    # print (object_summary.key)
#     if object_summary.key=='testing.jpeg':
#         print(object_summary.key)
from PIL import Image
img = Image.open('static/index.jpeg')
img.show()
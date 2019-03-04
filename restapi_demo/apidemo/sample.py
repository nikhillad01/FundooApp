from restapi_demo.apidemo.models import  Notes
from datetime import datetime


item=Notes.objects.filter(user_id=49,reminder=datetime.datetime.today())

import redis
"""This file contains details about redis connection 

    StrictRedis does not provide compatibility for older versions of redis.py
    Do you need backwards compatibility ? Use Redis
    
"""


r= redis.StrictRedis(host='localhost', port=6379, db=0)

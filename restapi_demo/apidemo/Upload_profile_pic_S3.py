import self as self
from services import redis_info
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
a=redis_info.get_token(self,'token')

redis_info.set_token(self,'b','value of b')
b=redis_info.get_token(self,'b')
#print(a)
print(b)
r.delete(b)
print(b)
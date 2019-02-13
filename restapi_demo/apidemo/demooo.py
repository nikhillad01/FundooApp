# import re
# #/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$/
# #^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$
# addressToVerify =input("Enter email")
# match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
# try:
#     if match == None:
#
# 	    print('Bad Syntax')
# 	    #raise ValueError('Bad Syntax')
# except ValueError:
#     print('Not Valid Email')
#
#
#
#     # match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

import socket
hostname = socket.gethostname()
print (hostname)
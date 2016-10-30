import re

def validateUsername(username):
     # check if string is alphanumeric, assumes string is clean
     return re.match(r'^\w+$', username)

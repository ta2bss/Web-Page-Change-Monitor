import hashlib

import requests

from datetime import datetime

now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M")
print (current_time)



url = 'http://www.ta2bss.com'
r = requests.get(url, allow_redirects=True)


f= open ("data","wb")
f.write(r.content)
f.close()

#open('data', 'wb').write(r.content)

def hash_file(filename):
   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

message = hash_file("data")

f=open ("records","a")
f.write(current_time+ " " +message+"\n")
f.close()

print(message)


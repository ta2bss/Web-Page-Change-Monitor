import requests
import os
url = 'https://nodes.guru/'
r = requests.get(url, allow_redirects=True)
f= open ("data","wb")
f.write(r.content)
f.close()

file = open("data")
file.seek(0, os.SEEK_END)
print("Size of file is :", file.tell(), "bytes")
file.close()
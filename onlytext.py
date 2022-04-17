import hashlib
from bs4 import BeautifulSoup as bs
import requests_html
from datetime import datetime

simdi = datetime.now()
su_an = simdi.strftime("%Y-%m-%d %H:%M")


# .htm , .html , .shtml , .asp , .pl , .cgi , .jsp. , php
s = requests_html.HTMLSession()
target = "https://nodes.guru/"
page = s.get(target)
soup=bs(page.text,'lxml')
contents = soup.get_text()
hash_object = hashlib.md5(contents.encode())
print(hash_object.hexdigest())

f=open ("data","a")
f.write(su_an+" "+target +"==>"+ hash_object.hexdigest()+"\n")
f.close()

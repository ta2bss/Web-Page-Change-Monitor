import hashlib
from bs4 import BeautifulSoup as bs
import requests_html
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M")


# .htm , .html , .shtml , .asp , .pl , .cgi , .jsp. , php

s = requests_html.HTMLSession()
target = ["https://nodes.guru/"  , "https://nodes.guru/subspace/setup-guide/en" ,"https://www.milliyet.com.tr/"]

for x in (range(len(target))):
    page = s.get(target[x])
    soup=bs(page.text,'lxml')
    contents = soup.get_text()
    hash_object = hashlib.md5(contents.encode())
    print(hash_object.hexdigest())

    f=open ("history","a")
    f.write(target[x] +" --> "+ date_time+" --> "+ hash_object.hexdigest()+"\n")
    f.close()

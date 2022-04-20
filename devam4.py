import sqlite3
import hashlib
from bs4 import BeautifulSoup as bs
import requests_html
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M")

# .htm , .html , .shtml , .asp , .pl , .cgi , .jsp. , php

s = requests_html.HTMLSession()
target = ["https://nodes.guru"  , "https://nodes.guru/subspace/setup-guide/en", "https://nodes.guru/aptos/setup-guide/en" ,"https://stackoverflow.com/" ]

for x in (range(len(target))):
    page = s.get(target[x])
    soup=bs(page.text,'lxml')
    contents = soup.get_text()

    pagecontent = target[x]
    pagecontent = pagecontent.replace(":","").replace("/","").replace("https","").replace("http","")
    hash_object = hashlib.md5(contents.encode())

    f=open ("data","a")
    f.write(target[x] +" --> "+ date_time+" --> "+ hash_object.hexdigest()+"\n")
    f.close()

    f=open (pagecontent +".dat","w")
    f.write(contents+"\n"+hash_object.hexdigest())
    f.close()



f=open ("data","r")
d = open ("datasorted","w")
for line in sorted(f):
    d.write(line)
f.close()
d.close()


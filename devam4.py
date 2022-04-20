import sqlite3
import hashlib
from bs4 import BeautifulSoup as bs
import requests_html
from datetime import datetime
import os
import sys
import pathlib


PageFolder = 'Datas/Pages'
Deletingoldfiles = os.listdir(PageFolder)

for item in Deletingoldfiles:
    if item.endswith(".old"):
        os.remove(os.path.join(PageFolder, item))



for filename in os.listdir(PageFolder):
    infilename = os.path.join(PageFolder,filename)
    if not os.path.isfile(infilename): continue
    oldbase = os.path.splitext(filename)
    newname = infilename.replace('.new', '.old')
    output = os.rename(infilename, newname)







pathDatas = "Datas"
pathPages = "Datas1\Pages"

try:
    os.mkdir(pathDatas)
except:
    pass
try:
    os.mkdir(pathPages)
except:
    pass

now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M")

#FOR  .htm , .html , .shtml , .asp , .pl , .cgi , .jsp. , php PAGES
s = requests_html.HTMLSession()

target = ["https://nodes.guru"  , "https://nodes.guru/subspace/setup-guide/en", "https://nodes.guru/aptos/setup-guide/en"  ]

for x in (range(len(target))):
    page = s.get(target[x])
    soup=bs(page.text,'lxml')
    contents = soup.get_text()
    encodedcontents = contents.encode()
    pagename = target[x]
    pagename = pagename.replace(":","").replace("/","").replace("https","").replace("http","")
    hash_object = hashlib.md5(encodedcontents)

    f=open ("Datas\\data", "a")
    f.write(target[x] +" --> "+ date_time+" --> "+ hash_object.hexdigest()+"\n")
    f.close()
    stringencodedcontents = str (encodedcontents)
    stringencodedcontents = stringencodedcontents.replace("\\n"," ").replace("\\t"," ")
    f=open ("Datas\\Pages\\"+pagename +".new","w")
    f.write("Date-Time:"+date_time+"\nPageHash:===>"+hash_object.hexdigest()+"<==="+"\n"+stringencodedcontents)
    f.close()



f=open ("Datas\\data", "r")
d = open ("Datas\\datasorted", "w")
for line in sorted(f):
    d.write(line)
f.close()
d.close()


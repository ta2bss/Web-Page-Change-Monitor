import hashlib
import re
import time

from bs4 import BeautifulSoup as bs
import requests_html
from datetime import datetime
import os

PageFolder = r'Datas/Pages'
Folder_Compilation = os.listdir(PageFolder)

for filename in Folder_Compilation:
    if filename.endswith(".old"):
        os.remove(os.path.join(PageFolder, filename))

for filename in Folder_Compilation:
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

targeturls = ["https://api.nodes.guru/aptos_update.sh","https://nodes.guru"  , "https://nodes.guru/subspace/setup-guide/en", "https://nodes.guru/aptos/setup-guide/en"  ]

for url in (range(len(targeturls))):
    page = s.get(targeturls[url])
    soup=bs(page.text,'lxml')
    pagecontents = soup.get_text()
    encoded_page_contents = pagecontents.encode()
    pagename = targeturls[url]
    pagename = pagename.replace(":","").replace("//","").replace("https","").replace("http","").replace("/","_")
    hash_object = hashlib.md5(encoded_page_contents)

    f=open ("Datas/history", "a")
    f.write(targeturls[url] +" --> "+ date_time+" --> "+ hash_object.hexdigest()+"\n")
    f.close()
    string_encoded_page_contents = str (encoded_page_contents)
    string_encoded_page_contents = string_encoded_page_contents.replace("\\n"," ").replace("\\t"," ")
    f=open ("Datas\\Pages\\"+pagename +".new","w")
    f.write("Date-Time:"+date_time+"\nPageHash:===>"+hash_object.hexdigest()+"<==="+"\n"+string_encoded_page_contents)
    f.close()


f= open("Datas/history","r")
linenumbers = len(f.readlines())
f.close()
print ("History Line Numbers: ",linenumbers)
if linenumbers > 70:
    f = open("Datas/history", "r+")
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    f.writelines(lines[10:])
    f.close()



f=open ("Datas/history", "r")
d = open ("Datas/sortedhistory", "w")
for line in sorted(f):
    d.write(line)
f.close()
d.close()

filelist =[]
for filename in Folder_Compilation:
    filelist.append(filename)

print (filelist)


for filename in filelist:
    f= open ("Datas/Pages/"+filename,"r")
    icerik = f.readlines()
    print(icerik)
    f.close

filenumber= len(filelist)
print ("File Number: ",filenumber)


import hashlib
import re
import time

from bs4 import BeautifulSoup as bs
import requests_html
from datetime import datetime
import os

#Date and Time module
now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M")


#specifying folders
PagesFolder = r'Datas/Pages'
ControlFolder = r'Datas/Control'
DatasFolder = r'Datas'

#Creating Working Folders if they don't exist
try:
    os.mkdir(DatasFolder)
except:
    pass
try:
    os.mkdir(PagesFolder)
except:
    pass
try:
    os.mkdir(ControlFolder)
except:
    pass

Folder_Pages = os.listdir(PagesFolder)
Folder_Control = os.listdir(ControlFolder)

#Deleting control files on every run
for filename in Folder_Control:
    if filename.endswith(".ctrl"):
        os.remove(os.path.join(ControlFolder, filename))

#Deleting old contents files on every run
for filename in Folder_Pages:
    if filename.endswith(".old"):
        os.remove(os.path.join(PagesFolder, filename))

#Renaming previos runs new content files as current runs old contents files
for filename in Folder_Pages:
    infilename = os.path.join(PagesFolder,filename)
    if not os.path.isfile(infilename): continue
    oldbase = os.path.splitext(filename)
    newname = infilename.replace('.new', '.old')
    output = os.rename(infilename, newname)

s = requests_html.HTMLSession()

#Web Pages to Moniror
targeturls = ["https://nodes.guru/aptos/setup-guide/en","https://nodes.guru","https://testnet.run/","https://testnet.run/services/23","https://testnet.run/"]


###### the codes have been edited up to this point
for url in (range(len(targeturls))):
    page = s.get(targeturls[url])
    soup=bs(page.text,'lxml')
    pagecontents = soup.get_text()
    pagecontents=pagecontents.replace("ü","u").replace("ı","i").replace("Ü","U").replace("Ğ","G").replace("ğ","g").replace("İ","I").replace("Ş","S").replace("ş","s").replace("ö","o").replace("Ö","O").replace("Ç","C").replace("ç","c")
    encoded_page_contents = pagecontents.encode()


    pagename = targeturls[url]
    pagename = pagename.replace(":","").replace("//","").replace("https","").replace("http","").replace("/","_")
    hash_object = hashlib.md5(encoded_page_contents)

    f=open ("Datas/history", "a")
    f.write(targeturls[url] +" --> "+ date_time+" --> "+ hash_object.hexdigest()+"\n")
    f.close()

    f=open ("Datas\\Pages\\"+pagename +".new","w")
    f.write("Date-Time:"+date_time+"\nPageHash:===>"+hash_object.hexdigest()+"<==="+"\n"+pagecontents)
    f.close()


f= open("Datas/history","r")
linenumbers = len(f.readlines())
f.close()
#print ("History Line Numbers: ",linenumbers)
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
for filename in Folder_Pages:
    filelist.append(filename)

#print (filelist)


for filename in filelist:
    f= open ("Datas/Pages/"+filename,"r")
    contents = f.readlines()
    #print(contents)
    f.close

filenumber= len(filelist)
#print ("File Number: ",filenumber)

for i in (filelist):

    i = i [:-4]

    n = open ("Datas/Pages/"+i+".new","r")
    nhashline = n.readlines()
    nhashcode = (re.search("===>(.+?)<===",nhashline[1]).group(1))
    n.close()

    o = open("Datas/Pages/" + i + ".old", "r")
    ohashline = o.readlines()
    ohashcode = (re.search("===>(.+?)<===", ohashline[1]).group(1))
    o.close()

    #print("new",i,nhashcode)
    #print("old",i,ohashcode)

    f= open ("Datas/Control/"+i+".ctrl","a")
    f.write(nhashcode+"\n")
    f.write(ohashcode+"\n")
    f.close()

    f= open ("Datas/Control/"+i+".ctrl","r")
    data = f.readlines()
    if (len(data)) > 2:
        continue

    if data[0] != data[1] :

        # Open File in Read Mode
        file_1 = open('Datas\Pages\\'+i+'.new', 'r')
        file_2 = open('Datas\Pages\\'+i+'.old', 'r')

        print("Comparing files ", " new " + 'Datas\Pages\\'+i+'.new',
              " old " + 'Datas\Pages\\'+i+'.old', sep='\n')

        file_1_line = file_1.readline()
        file_2_line = file_2.readline()

        # Line Counter
        line_no = 1

        print()

        with open('Datas\Pages\\'+i+'.new') as file1:
            with open('Datas\Pages\\'+i+'.old') as file2:
                same = set(file1).intersection(file2)

        print("Difference Lines in Both Files")
        while file_1_line != '' or file_2_line != '':

            # Removing whitespaces
            file_1_line = file_1_line.rstrip()
            file_2_line = file_2_line.rstrip()

            # Compare the lines from both file
            if file_1_line != file_2_line:

                # otherwise output the line on file1 and use new sign
                if file_1_line == '':
                    print("new", "Line-%d" % line_no, file_1_line)
                else:
                    print("new-", "Line-%d" % line_no, file_1_line)

                # otherwise output the line on file2 and use # sign
                if file_2_line == '':
                    print("old", "Line-%d" % line_no, file_2_line)
                else:
                    print("old+", "Line-%d" % line_no, file_2_line)

                # Print a empty line
                print()

            # Read the next line from the file
            file_1_line = file_1.readline()
            file_2_line = file_2.readline()

            line_no += 1

        file_1.close()
        file_2.close()
        log=open("log.txt","a")
        log.write(date_time+" "+i+" CHANGED \n")
        log.close()

    f.close()
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
dateonly = now.strftime("%Y-%m-%d")
timeonly = now.strftime("%H:%M")


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

dailylogs = open ("Datas\\Control\\"+ dateonly +"-logs","a")

dailylogs.write("******"+"\n")
dailylogs.write(timeonly+"\n")
dailylogs.write("******"+"\n")
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
targeturls = ["https://www.google.com" , "https://stackoverflow.com/" ]


#Check above web pages in for loop
for url in (range(len(targeturls))):
    print ("Checking ",targeturls[url])
    dailylogs.write ("Checking "+targeturls[url]+"\n")

    #starting chronometer
    start = (time.perf_counter())
    page = s.get(targeturls[url])
    soup=bs(page.text,'lxml')
    pagecontents = soup.get_text()

    #remove non-ASCII characters
    pagecontents= re.sub(r'[^\x00-\x7f]', r'',pagecontents)

    encoded_page_contents = pagecontents.encode()
    pagename = targeturls[url]
    pagename = pagename.replace(":","").replace("//","").replace("https","").replace("http","").replace("/","_")
    hash_object = hashlib.md5(encoded_page_contents)

    #creating and writing history file
    f=open ("Datas/history", "a")
    f.write(targeturls[url] +" --> "+ date_time+" --> "+ hash_object.hexdigest()+"\n")
    f.close()

    #creating and writing webpages to files with new content
    f=open ("Datas\\Pages\\"+pagename +".new","w")
    f.write("Date-Time:"+date_time+"\nPageHash:===>"+hash_object.hexdigest()+"<==="+"\n"+pagecontents)
    f.close()
    #stop chronometer and calculate time
    end = (time.perf_counter())
    print("Checked ", targeturls[url]," at ", round((end-start),2) , " seconds.")
    dailylogs.write("Checked "+ targeturls[url]  + "\n")
    print ("-------------")
    dailylogs.write("----------------"+ "\n")



f= open("Datas/history","r")
linenumbers = len(f.readlines())
f.close()
#Limit size of history file
if linenumbers > 70:
    f = open("Datas/history", "r+")
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    f.writelines(lines[10:])
    f.close()


#Sort Alphapatical history file
f=open ("Datas/history", "r")
d = open ("Datas/sortedhistory", "w")
for line in sorted(f):
    d.write(line)
f.close()
d.close()

# Create file list
filelist =[]
for filename in Folder_Pages:
    filelist.append(filename)

for filename in filelist:
    try:

        f= open ("Datas/Pages/"+filename,"r")
        contents = f.readlines()
        f.close

    except:
        continue

filenumber= len(filelist)

for i in (filelist):
    i = i [:-4]
    try:
        n = open ("Datas/Pages/"+i+".new","r")
        nhashline = n.readlines()
        nhashcode = (re.search("===>(.+?)<===",nhashline[1]).group(1))
        n.close()
    except:
        continue
    o = open("Datas/Pages/" + i + ".old", "r")
    ohashline = o.readlines()
    ohashcode = (re.search("===>(.+?)<===", ohashline[1]).group(1))
    o.close()

    f= open ("Datas/Control/"+i+".ctrl","a")
    f.write(nhashcode+"\n")
    f.write(ohashcode+"\n")
    f.close()

    f= open ("Datas/Control/"+i+".ctrl","r")
    data = f.readlines()
    if (len(data)) > 2:
        continue

    #if contents are different
    if data[0] != data[1] :

        # Read old and new content files
        newfile = open('Datas\Pages\\'+i+'.new', 'r')
        oldfile = open('Datas\Pages\\'+i+'.old', 'r')

        print("Comparing files ", " new " + 'Datas\Pages\\'+i+'.new'," old " + 'Datas\Pages\\'+i+'.old', sep='\n')

        dailylogs.write ("\n"+"COMPARING FILES"+"\n"+"Datas\\Pages\\" +i+ ".new"+"\n" "Datas\\Pages\\" + i + ".old"+ "\n"+"\n")

        newfile_line = newfile.readline()
        oldfile_line = oldfile.readline()

        # Line Counter
        line_no = 1
        print()
        dailylogs.write("")

        with open('Datas\Pages\\'+i+'.new') as file1:
            with open('Datas\Pages\\'+i+'.old') as file2:
                same = set(file1).intersection(file2)

        print("Difference Lines in Both Files")
        while newfile_line != '' or oldfile_line != '':

            # Removing spaces
            newfile_line = newfile_line.rstrip()
            oldfile_line = oldfile_line.rstrip()

            # Compare the lines
            if newfile_line != oldfile_line:

                # otherwise output the line on file1
                if newfile_line == '':
                    print("new content:", "Line-%d" % line_no, newfile_line)
                    dailylogs.write(("new content :"+ "Line-%d " % line_no+ newfile_line+"\n"))
                else:
                    print("new content:", "Line-%d" % line_no, newfile_line)
                    dailylogs.write("new content :"+ "Line-%d " % line_no + newfile_line+"\n")

                # otherwise output the line on file2
                if oldfile_line == '':
                    print("old content:", "Line-%d" % line_no, oldfile_line)
                    dailylogs.write("old content :"+ "Line-%d " % line_no + oldfile_line +"\n")
                else:
                    print("old content:", "Line-%d" % line_no, oldfile_line)
                    dailylogs.write("old content :" + "Line-%d " % line_no + oldfile_line +"\n")

                print ("")
                dailylogs.write("\n")
            # Read Next line
            newfile_line = newfile.readline()
            oldfile_line = oldfile.readline()

            # Line Counter
            line_no += 1

        newfile.close()
        oldfile.close()
        log=open("log.txt","a")
        log.write(date_time+" "+i+" CHANGED \n")
        log.close()

    f.close()
    dailylogs.close()
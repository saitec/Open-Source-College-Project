# This program will list all the links from a webpage and save them
# into a file and offer the possibility to download specific kind of files based on 
# their extensions
 
import sys
import urllib2
import re
import os
 
outputFile = './tmp.txt'
 
def updateRelativeLinks(urlname):
    global outputFile
    updatedOutputFile = './' + urlname[7:] + '.txt'
    count = 0
    try:
        of = open(outputFile, 'r')
        off = open(updatedOutputFile, 'w')
 
        for line in of:
            if not 'http' in line:
                #sometime slash is missing as first char in relative URL
                if line[0] != '/':          
                    line = '/' + line
                count += 1
                newline = urlname + line
                off.write(newline)
                print 'Find [',count,']: ', newline.replace('\n','')
            else:
                off.write(line)
 
        of.close()
        off.close()
        os.remove(outputFile)
        outputFile = updatedOutputFile
 
    except:
        print 'updateRelativeLinks error'
        of.close()
        off.close()
 
def findLinks(url):
    global outputFile
    
    try:
        if url[0:7] != 'http://':
            url = "http://" + url
 
        of = open(outputFile, 'w')
 
        f = (urllib2.urlopen(url)).read()         #Open the URL
        k = re.findall('(src|href)="(\S+)"',f)    #Find links in the source
        k = set(k)                                #Store all elements in a dictionnary
 
        for x in k:
            if len(x[1]) > 2:
                of.write(x[1]+'\n')               #Store each links into the file
 
        of.close()
 
        updateRelativeLinks(url)
 
    except:
        print 'URL not found'
 
def download(extensions):
    global outputFile
 
    extList = extensions.split(',')
    of = open(outputFile, 'r')
 
    if not os.path.exists('./'+outputFile[2:-4]):
        os.makedirs('./'+outputFile[2:-4])
 
    for line in of:
        for ext in extList:
            if '.'+ext in line:
                try:
                    rawData = (urllib2.urlopen(line).read())
                    filename = line.split('/')
                    dlData = open(('./'+outputFile[2:-4]+'/'+filename[len(filename)-1]).replace('\n',''), 'w')
                    dlData.write(rawData)
                    print 'Downloaded : ' + line.replace('\n','')
                    dlData.close()
                except:
                    print 'Download error with ', line
                    continue
 
    of.close()    
 
def usage():
    print """
-------------------------------------------------------------------
|usage:                                                           |
|python webLinks.py full_url [ext1,ext2,..,extn]                  |
|example:-                                                        |
|python webLinks.py http://www.example.com/hello-world png,jpg,wmv|
-------------------------------------------------------------------
"""
 
if __name__ == '__main__':
    print """
--------------------------------------------------------------
| All links are stored in a file named with the URL          |
| and if specified, all downloaded files are in a dedicated  |
| folder                                                     |
--------------------------------------------------------------
"""
    argCount = len(sys.argv)
 
    if argCount != 2 | argCount != 3:
        usage()
    else:
        findLinks(sys.argv[1])
 
        if(argCount == 3):
            download(sys.argv[2])
#from http://bookworm-project.github.io/Docs/input.txt.html

import os

import xml.dom.minidom

import urllib

import sys

import magic

import re

import wget

#from https://github.com/euske/pdfminer/tree/b0e035c24fa062cd55cfd55ffc12bc3aa60a4ef6 download the zip and python setup.py install

from cStringIO import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from pdfminer.converter import TextConverter

from pdfminer.layout import LAParams

from pdfminer.pdfpage import PDFPage

import json

import subprocess

#encoding

import codecs

def createSearchString(year, uni, url):
    #create dom object
    doc = xml.dom.minidom.Document()
    #create anchor element
    anchor = doc.createElement('a')
    #add attributes to element
    anchor.attributes['href']= url
    anchor.attributes['target']= "_blank"
    #create text for inside the element
    txt = doc.createTextNode("%s document from %s" % (year, uni))
    anchor.appendChild(txt)
    return anchor.toxml()



def removeEverythingButAlphaNumeric(stringToClean):

    textFinal = re.sub(r'\W+', ' ', stringToClean)

    return textFinal



#from http://www.binpress.com/tutorial/manipulating-pdfs-with-python/167

def convert(fname1, pages=None):

    if not pages:

        pagenums = set()

    else:

        pagenums = set(pages)

    output = StringIO()

    manager = PDFResourceManager()

    converter = TextConverter(manager, output, laparams=LAParams())

    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname1, 'rb')

    for page in PDFPage.get_pages(infile, pagenums):

        interpreter.process_page(page)

    infile.close()

    converter.close()

    text = output.getvalue()

    output.close

    #TODO Write function which removes all but the alphanumeric strings (new line, tab and carriage returns etc)

    return removeEverythingButAlphaNumeric(text)



def createTextFilename(filePathOnly, year, uni, extensionRequired):

    orig = filePathOnly + "_" + year + "_" + uni

    orig2 = re.sub('[/ \s\/]', '_', orig)

    if ( extensionRequired == True ):

        return orig2 + ".txt"

    else:

        return orig2



def returnMimeType(locationOfFile):

	m = magic.open(magic.MAGIC_MIME_TYPE)

	m.load()

	mimeType = m.file(locationOfFile)

	return mimeType



def createJsonCatalogTxt(year, uni, filename, searchString):

    date = year

    #from https://freepythontips.wordpress.com/2013/08/08/storing-and-loading-data-with-json/

    jsonObject1 = {u"date": int(date), u"uni": uni, u"filename": filename, u"searchstring": searchString}

    return json.dumps(jsonObject1)



def doesFileExist(URL, root):

    #strip filename from url

    URLSplit = URL.split(os.sep)

    URLFile = URLSplit[-1]

    print "Checking to see if the file already exists"

    if os.path.exists(os.path.join(root, URLFile)):

        print "It appears that we have already downloaded that file"

        return True

    else:

        print "Nope we do not have that file, yet!"

        return False



def fetchPdf(URL, root):

    URLSplit = URL.split(os.sep)

    URLFile = URLSplit[-1]

    pathToCheck = os.path.join(root, URLFile)

    print "Checking to see if the file already exists"

    if os.path.exists(pathToCheck):

        print "It appears that we have already downloaded that file"

        return pathToCheck

    else:

        #get wget from https://pypi.python.org/pypi/wget and run the setup.py file using "python setup.py install" after unzipping

        #gets the PDF from the URL and saves it to the directory to which root is pointing

        print "It appears that we do not have that file yet"

        f = wget.download(URL, root)

        print "File downloaded ..."

        print "... checking to see if the file is a PDF"

        if returnMimeType(f) == 'application/pdf':

            print "The file is a PDF"

            return f

        else:

            return False



def lowerAndStrip(URL):

    #TODO write a more comprehensive clean up module 

    URL1 = URL.lower()

    URL2 = URL1.strip()

    return str(URL2)





currentDir = os.getcwd()

print "Current working directory is %s" % (currentDir)

print "Creating output environment"

print "Establishing the path to the output files"
pTrt = os.path.join(currentDir, "files", "texts", "raw")
print "Checking to see if the raw files directory exists"
if (not os.path.exists(pTrt)):
    print "The raw files directory does not exists so we will create it now"
    os.makedirs(pTrt)
else:
    print "We already have a raw files directory"
    
os.makedirs(os.path.join(currentDir, "files", "metadata"))

print "Copying our field_descriptions.json file from %s to the files/metadata dir " % (currentDir)

subprocess.call(['cp', 'field_descriptions.json', 'files/metadata/'])

print "Creating the jsoncatalog.txt file"

jsonCatalogFile = codecs.open(os.path.join(currentDir, "files", "metadata" , "jsoncatalog.txt"), 'wb', "utf-8")

for root, dirs, files in os.walk(os.path.join(currentDir, "bookworm_transform")):

    for file in files:

        textFileLocation = os.path.join(root, file)

        if returnMimeType(textFileLocation) == 'text/plain':

            with open(textFileLocation) as theTextFile:

                for line in theTextFile:

                    cleanLine = line.strip()

                    if cleanLine.endswith(".pdf"):

                        print "Processing line %s " % (cleanLine)

                        #TODO write break out in the event that file retured is not a pdf

                        pdfFileLocation = fetchPdf(cleanLine, root)

                        pathToSplit = pdfFileLocation

                        print "Splitting the path %s " % (pdfFileLocation)

                        splitPathArray = pathToSplit.split(os.sep)

                        print "The split path looks like this ..."

                        print splitPathArray

                        startIndex = splitPathArray.index('bookworm_transform')

                        print "The start index of the split path is %s " % (str(startIndex))

                        year = splitPathArray[startIndex + 1]

                        print "The year is %s " % (str(year))

                        uni = splitPathArray[startIndex + 2]

                        print "The uni is %s " % (uni)

                        filePathOnly, fileExtension = os.path.splitext(pdfFileLocation)

                        print "File path only is %s and file extension is %s" % (filePathOnly, fileExtension)

                        fn = createTextFilename(filePathOnly, year, uni, False)

                        print "The filename for the text withOUT an extension is %s " % (fn)

                        #create text file name with a text extension

                        fnExt = createTextFilename(filePathOnly, year, uni, True)

                        print "The filename for the text WITH an extension is %s " % (fnExt)
                        
                        rawTt = os.path.join(currentDir, "files", "texts", "raw", fnExt)
                        
                        print "Checking to see if we have already extracted the text for this document"
                        if (not os.path.exists(rawTt)):
                            print "Looks like we have to extract the text for this document"
                            rawTextFile = codecs.open(rawTt, 'wb', "utf-8")

                            print "Extracting text from PDF file and writing to text file."

                            rawTextFile.write(convert(pdfFileLocation))

                            rawTextFile.close()

                        #TODO scrape search and URL string from data
                        else:
                            print "We have already extracted the text for this file"

                        searchString = createSearchString(year, uni, cleanLine)
                        #create json catalog file

                        print "Writing to the jsoncatalogfile"

                        jsonCatalogFile.write(createJsonCatalogTxt(year, uni, fn, searchString))

                        jsonCatalogFile.write("\n")

                        print "*"

                        print "Finished processing %s " % (pdfFileLocation)

print "Finished processing ALL files"

jsonCatalogFile.close()

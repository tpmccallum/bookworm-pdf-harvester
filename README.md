# bookworm-pdf-harvester
A Python program which will fetch PDF files from the web in bulk and create a zip file for Bookworm.

This was written so that many PDF documents could be fetched over the open web using lists of URLs. If you know of publicly available PDF documents which you want to ingest into the < https://github.com/Bookworm-project > this may get the job done.

I would like to create a GitBook soon but for now you can take a look at the very very simplistic instructions below

Instructions
Go to a clean area on Ubuntu Linux eg /home/user

place the python file in the /home/user folder eg /home/user/driver.py 

create a folder called bookworm_transform eg /home/user/bookworm_transform

create a folder inside bookworm_transform for each year you wish to analyse 

create a folder inside each "year" folder for each entity you would like to analyse

eg
'''
|bookworm_transform
         |--- 2010          2011       2012
               | |            |         |
             USQ  UNE       UNISA      USC



place a text file with a list of URLs (one per line) which point to online PDFs. bookworm_transform/2010/USQ/listOfPDFUrls.txt

ensure that there are no files in any of the other folders (only the lowers level)

run the python file 

eg 

ubuntu:~$ cd /home/user

ubuntu:~$ python driver.py 

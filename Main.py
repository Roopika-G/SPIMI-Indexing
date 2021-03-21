import tracemalloc
import psutil
from Merge import blockdefinition
from spimiinvert import spimiinvert
from pathlib import Path
import sys
import json
import os
import glob
import string
import ast
import unidecode
from unidecode import unidecode
import re
import nltk
from nltk import word_tokenize
import time
from hurry.filesize import size
import collections
from collections import OrderedDict
sc = ["//","/",",,",'”','/','`','?','!',',','+','-','.','?','!','\'\'','\'','$','^','~',':',';','"','{','}','&','(',')','@','*','>','<','#',"''",'``','...','..','[',']','|','','=','_','%',"__","___","'","'b"]
#INITIALIZING ALL NEEDED VARIABLES
totalfiles =0
#block_number = 0
countersum = 0
documents =dict()
filesize = 0       
filelist = []
comparefilelist =[]
filenum = 0
ALLFILE =[]
linguitictime =[]
#INITIALIZING THE STEMMING FOR DATA CLEANING
stemmer = nltk.PorterStemmer()
#GETTING THE TOTAL NUMBER OF TEXT FILES IN THE FOLDER

startcode = time.process_time()
BASEPATH = input("Please provide the path of the directory containing the text file : ")
ACTUALFILESIZE = input("Please Provide the block size (in Bytes) : ") #55000
ALLOWEDSIZE = 2*int(ACTUALFILESIZE)
#PRINTING THEM HERE
print("The Base Path is : ", BASEPATH ," & The Block Size is : ", ACTUALFILESIZE, "\n")
entries = Path(BASEPATH)
for entry in entries.iterdir():
            totalfiles = totalfiles+1
            #print(totalfiles)
for entry in entries.iterdir():
            ALLFILE.append(entry.name)



print("=============== Retriving documents... =============== ")
startret = time.process_time()

while filenum != totalfiles:
        #FOR EACH TEXT FILE IN THE DIRECTORY
        for FILE in ALLFILE:
                if len(ALLFILE) == 0:
                                break
                # COMPARING IT WITH LIST 
                onefile = FILE
                filesize = filesize + os.stat(BASEPATH + onefile).st_size
                if filesize <= int(ALLOWEDSIZE):
                                        filenum = filenum + 1
                                        filelist.append(onefile) 
                else:
                        break
#READING THE FILE CONTENTS AND STORING IT IN A DICT
        endret = time.process_time()
        rettime = endret - startret
        print("Time Taken for Document Retrival: ", rettime,"Sec")
        print("=============== Preprocessing documents... ===============")
        starttok = time.process_time()
        for infile in filelist:             
                        xfile = open(BASEPATH + infile, encoding = 'UTF-8')
                        newid = infile
                        newid =newid.split(".txt",1)[0]
                        tokens = word_tokenize(xfile.read())
                        tokens = [token.lower() for token in tokens]
                        tokens = [token for token in tokens if not token in string.punctuation]
                        tokens = [token.replace("(<br/>)", "") for token in tokens]
                        tokens = [token.replace('(<a).*(>).*(</a>)', '') for token in tokens]
                        tokens = [token.replace('(&amp)', '') for token in tokens]
                        tokens = [token.replace('(&gt)', '') for token in tokens]
                        tokens = [token.replace('(&lt)', '') for token in tokens]
                        tokens = [token.replace('(\xa0)', '') for token in tokens]
                        tokens = [re.sub(r"([.,!?])", r" \1 ", token) for token in tokens]
                        tokens = [re.sub(r"[^a-zA-Z.,!?]+", r" ", token) for token in tokens]
                        tokens = [token for token in tokens if not any(c in sc for c in token)]      
                        tokens = [stemmer.stem(token) for token in tokens]
                        tokens = [token for token in tokens if not any(c.isdigit() for c in token)]
                        tokens = [re.sub(r'\b\w{1}\b', '', token) for token in tokens]
                        tokens = [token.strip() for token in tokens]
                        tokens = [token.strip(" ") for token in tokens]
                        tokens = list(filter(None, tokens))
                        documents[newid] = tokens
        endtok = time.process_time()
        tokentime = endtok - starttok
        linguitictime.append(tokentime)
        print("Time Taken to tokenize at each block  : ", tokentime,"Sec")
        #SPIMI INVERT FUNCTION CALLED
        spimiinvert(documents,ACTUALFILESIZE)
        for comp in filelist:
                ALLFILE.remove(comp)
        filelist.clear()
        filesize = 0
        documents.clear()
        print("This is the number of files : ", filenum,"\n")

endcode = time.process_time()
codetime = endcode-startcode
print("\n")
print("Total Time taken until Merge Process : ", codetime,"Sec \n")
stfullcode = time.process_time()
#MERGE FUNCTION CALLED
#tracemalloc.start()
blockdefinition()
#current, peak = tracemalloc.get_traced_memory()
#print(f" After Merge : Current memory usage is {current / 10**6}MB")
#tracemalloc.stop()
edfullcode = time.process_time()
fullmergecode = edfullcode - stfullcode
print("Time taken for entire Merge process : ", fullmergecode,"Sec \n")
fullcodetime = codetime + fullmergecode
print("Entire Time Taken : ", fullcodetime,"Sec")
summ =0
for ind in linguitictime:
        summ = summ+ind
print("Time Taken for linguistic processing : ",summ,"Sec")










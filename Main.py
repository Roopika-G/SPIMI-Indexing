import tracemalloc
import psutil
from Merge import blockdefinition
from os import listdir
#from MERGE1 import blockMerge
from spimiinvert import spimiinvert
from pathlib import Path
import RANKING as BM25
import sys
import json
import _pickle as cPickle
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
#nltk.download('words')
#words = set(nltk.corpus.words.words())
#NEW ADDED LINE#############################################################################
def save_collection_stats(N, doc_length_dict):
     total_docs_length = 0
     for key, value in doc_length_dict.items():
         total_docs_length += value
     avg_doc_length = total_docs_length / N
     with open("DISK/collection_stats", "wb") as stats_file:
             #REPLACE PICKLE.HIGHESTPROTOCOL WITH -1
         cPickle.dump((N, doc_length_dict, avg_doc_length), stats_file, -1)
     stats_file.close()


# def get_inverted_index(index_file):
#         index = dict()
#         indexFile = open("Merge/invert_actual_index.txt")
#         for line in indexFile:
#                 if not line == '':
#                         splits = line.split(' -----------> ')
#                         term = splits[0]
#                         postings = splits[1]
#                         index.update({term: postings})
#         inverted_index = dict(index)
#         #print(inverted_index)
#         return dict(inverted_index)
#sent = "Io andiamo to the beach with my amico."
#sent = " ".join(w for w in nltk.wordpunct_tokenize(sent) if w.lower() in words or not w.isalpha())
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
stopword = open('spacy.txt')
STOP_WPRDS = word_tokenize(stopword.read())
startcode = time.process_time()
BASEPATH = input("Please provide the path of the directory containing the text file : ")
ACTUALFILESIZE = input("Please Provide the block size (in Bytes) : ") #55000
ALLOWEDSIZE = 2*int(ACTUALFILESIZE)
print("The Base Path is : ", BASEPATH ," & The Block Size is : ", ACTUALFILESIZE, "\n")
entries = Path(BASEPATH)
# #NEW ADDED LINE#############################################################################
N = 0
# #NEW ADDED LINE#############################################################################
doc_length_dict = {}
for entry in entries.iterdir():
            #print("I AM JERE ", entry)
            totalfiles = totalfiles+1
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
                        # #NEW ADDED LINE#############################################################################
                        TEXT = xfile.read()
                        # #NEW ADDED LINE#############################################################################
                        N += len(TEXT)
                        # #NEW ADDED LINE#############################################################################
                        doc_length_dict[newid] = len(TEXT.split())
                        tokens = word_tokenize(TEXT)
                        #print("this is token: ", tokens)
                        tokens = [token.lower() for token in tokens]
                        #tokens = [word for word in tokens if not word in STOP_WPRDS] 
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
                        #tokens = [word for word in tokens if not word in STOP_WPRDS]     
                        tokens = [stemmer.stem(token) for token in tokens]
                        tokens = [token for token in tokens if not any(c.isdigit() for c in token)]
                        #tokens = [re.sub(r'\b\w{1}\b', '', token) for token in tokens]
                        tokens = [re.sub(r'\b\w{1}\b', '', token) for token in tokens]
                        tokens = [re.sub(r'\b\w{2}\b', '', token) for token in tokens]
                        tokens = [token.strip() for token in tokens]
                        tokens = [token.strip(" ") for token in tokens]
                        #tokens = [token for token  in tokens if token in words or not token.isalpha()]
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
save_collection_stats(N, doc_length_dict)
blockdefinition()
#blockMerge(open('index_blocks/'+block) for block in listdir('index_blocks/'))
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
q = BM25.SPIMIRanking()
#index_file = 'Merge/invert_actual_index.txt'
q.RankDocuments()















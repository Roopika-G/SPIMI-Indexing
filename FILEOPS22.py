import tracemalloc
import psutil
from pathlib import Path
#import RANKING as BM25
import sys
import json
import _pickle as cPickle
import os
import glob
import string
import ast
import unidecode
from unidecode import unidecode
import collections
from collections import OrderedDict  

def readIndexIntoMemory():
        index = OrderedDict()
        indexFile = open("Merge/invert_actual_index.txt")
        for line in indexFile:
                if not line == '':
                        splits = line.split(' -----------> ')
                        term = splits[0]
                        postings = splits[1]
                        index.update({term: postings})
        postingsCount = 0
        for i in index:
                postingsCount += len(index[i])
        return(index)
    
    
def readRankintomemory():
         index1 = {}
         indexFile = open("Merge/rank_file.txt")
         strindex = indexFile.read()
         index1 = json.loads(strindex)
         return(index1) 
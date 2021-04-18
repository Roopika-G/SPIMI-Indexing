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


def ranked_search():
    print("This query will return the top 20 results, using BM25 algorithm.")
    #inverted_index = get_inverted_index(index_file)

    while True: # keep running the program
        query = input("Enter a search query: ")
        matches = q.GetRankedResults(query)
        for match in matches[:20]:
            print("Document IDS with Ranking: %s Ranking Score: %s" % (str(match[0]), str(match[1])))




# single_keyword_query()
# multiple_and_keyword_query()
# multiple_or_keyword_query()
q = BM25.SPIMIRanking()
ranked_search()
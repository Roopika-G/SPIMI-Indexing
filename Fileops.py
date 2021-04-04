import collections
import json
import time
import tracemalloc
from collections import OrderedDict
import ast
import os



#final = dict()
#l = open('Merge/invert_index.txt')
#iterlist = (l.read().strip().split('\n'))
#for l2 in range (len(iterlist)):
            #ksplit = iterlist[l2].split(" -----------> ")# ['aa',[5,[1,2,3]]]
            #val = ksplit[0]
            #a = ksplit[1]
           # b = a.split("[")
            #c = b[2]
            #d = c.split("]]")
            #poslist = d[0]
            #final[val] = poslist

			
#def readIndexIntoMemory():
        #index = OrderedDict()
        #indexFile = open("Merge/invert_index.txt")
        #for line in indexFile:
                #if not line == '':
                        #splits = line.split(' -----------> ')
                        #term = splits[0]
                        #a = splits[1]
                        #b = a.split("[")  
                        #c = b[2]
                        #d = c.split("]]")
                        #postings = ast.literal_eval('['+ d[0] + ']') # convert a string list to a list
                        #index.update({term: postings})

        #postingsCount = 0

        #for i in index:
                #postingsCount += len(index[i])
        #return(index)


def readIndexIntoMemory():
        index = OrderedDict()
        indexFile = open("Merge/invert_actual_index.txt")
        for line in indexFile:
                if not line == '':
                        splits = line.split(' -----------> ')
                        term = splits[0]
                        a = splits[1]
                        b = a.split("[")  
                        c = b[2]
                        d = c.split("]]")
                        postings = ast.literal_eval('['+ d[0] + ']') # convert a string list to a list
                        index.update({term: postings})
        #print(index)		
        # Generate some stats about imported index
        postingsCount = 0
        # print 'Size of index: ' + str(len(index)) + '\n'
        for i in index:
                postingsCount += len(index[i])
        # print 'Number of total postings: ' + str(postingsCount) + '\n'
        return(index)
              
def getTotalSet(index):
    
     _total_Set = set()
     for key in (index):
           _postling_list = index[key]
           _postling_list = set(_postling_list)
           _total_Set = {*_total_Set, *_postling_list}
          
           
     #print("TS::::",len(_total_Set))
     return(_total_Set)
#readIndexIntoMemory()
def compressedstring():
        #index = OrderedDict()
        indexFile = open("Merge/index_cp_1.txt")
        compression_word =indexFile.read()
        #print(compression_word)
        # print 'Number of total postings: ' + str(postingsCount) + '\n'
        return(compression_word)
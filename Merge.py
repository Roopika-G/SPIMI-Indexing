from pathlib import Path
import sys
from os import listdir
import collections
from collections import OrderedDict
import ast
import json
import time
import tracemalloc

def blockdefinition():
    ALLBLOCKFILE =[]
    BLOCKSTOMERGE =0
    spimi_index = 'Merge/invert_index.txt'
    BLOCKPATH = 'index_blocks/'
    blockentries = Path('index_blocks/')
    for blockentry in blockentries.iterdir():
            BLOCKSTOMERGE = BLOCKSTOMERGE+1
    #print(BLOCKSTOMERGE)
    for blockentry in blockentries.iterdir():
            ALLBLOCKFILE.append(blockentry.name)
    blockMerge(ALLBLOCKFILE,BLOCKSTOMERGE,BLOCKPATH,spimi_index)

def blockMerge(ALLBLOCKFILE,BLOCKSTOMERGE,BLOCKPATH,spimi_index):
    print("=============== Merging SPIMI blocks into final inverted index... ===============")
    tracemalloc.start()
    Filewrite = open('Merge/invert_index.txt',"w+")
    iterlist = [] 
    startmerge = time.process_time()
    for BLOCKFILE in ALLBLOCKFILE:
        print("File Name:",BLOCKFILE)
        print("-- Reading into memory... ",BLOCKFILE.split(".txt",1)[0])
        
        finaldict={}


        l = open(BLOCKPATH + BLOCKFILE)
        Fileread = open('Merge/invert_index.txt') 
        Initialfile= Fileread.read()
        if(Initialfile.strip()):
             lst = Initialfile.strip().split('\n')
             for i in range(len(lst)):
                 val = lst[i].split(" -----------> ")
                 finaldict[val[0]] = val[1] 
        else:
           finaldict={}     


        iterlist = (l.read().strip().split('\n'))
        for l2 in range (len(iterlist)):
            ksplit = iterlist[l2].split(" -----------> ")# ['aa',[5,[1,2,3]]]
            #print(ksplit[0])
            #print("        ", ksplit[0])
            if(finaldict.get(ksplit[0])!= None):
                postlingvalold = json.loads (finaldict.get(ksplit[0])) # [5,[4,5,6]]
                newblock = json.loads(ksplit[1])
                for i in range (len(newblock[1])):
                 if newblock[1][i] not in postlingvalold[1]:
                   postlingvalold[1].append(newblock[1][i])
                postlingvalold[0] = postlingvalold[0]+newblock[0] # adding counter values
                finaldict[ksplit[0]] = str(postlingvalold)
            else:
                #print(ksplit[1])
                finaldict[ksplit[0]] = ksplit[1]   
        
        sorted(finaldict)
        
        
        Filewrite = open('Merge/invert_index.txt',"w+")
        for key,value in sorted(finaldict.items()):
             Filewrite.write(key+" -----------> "+ value + "\n")  
        print("Finished merging block: ",BLOCKFILE.split(".txt",1)[0]," and writing to disk")
        endmerge = time.process_time()
        eachmerge = endmerge -startmerge
        print("\n Time taken after each Block merge : ",eachmerge, "\n")
        Fileread.close()
        Filewrite.close()
        current, peak = tracemalloc.get_traced_memory()
        print(f" After merge : Current memory usage is {current / 10**6}MB")
        tracemalloc.stop()








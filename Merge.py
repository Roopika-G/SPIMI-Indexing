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
    compression()

def blockMerge(ALLBLOCKFILE,BLOCKSTOMERGE,BLOCKPATH,spimi_index):
    print("=============== Merging SPIMI blocks into final inverted index... ===============")
    tracemalloc.start()
    Filewrite = open('Merge/invert_index.txt',"w+")
    iterlist = [] 
    term=""
    current_term = ""
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
                current_term = ksplit[0]
                #_term_lenth = len(term)
                #_index_of_current_term = len(term)
                #(' _term_lenth', _term_lenth)
                term=term+current_term.capitalize()
                finaldict[ksplit[0]] = ksplit[1]   
        
        sorted(finaldict)
        
        
        Filewrite = open('Merge/invert_index.txt',"w+")
        Filewrite1 = open('Merge/invert_actual_index.txt',"w+")
        indexwriter1 = open('Merge/index_cp_1.txt',"w+")
        indexwriter1.write(term)
        for key,value in sorted(finaldict.items()):
             Filewrite.write(key+" -----------> "+ value + "\n")  
             Filewrite1.write(key+" -----------> "+ value + "\n") 
        print("Finished merging block: ",BLOCKFILE.split(".txt",1)[0]," and writing to disk")
        endmerge = time.process_time()
        eachmerge = endmerge -startmerge
        print("\n Time taken after each Block merge : ",eachmerge, "\n")
        Fileread.close()
        Filewrite.close()
        Filewrite1.close()
        indexwriter1.close()
        current, peak = tracemalloc.get_traced_memory()
        print(f" After merge : Current memory usage is {current / 10**6}MB")
        tracemalloc.stop()



def compression():
        indexReader = open('Merge/invert_index.txt') #to be moved
        compression_word_list = open('Merge/index_cp_1.txt')
        compression_word= compression_word_list.read()
        inverted_index_file= indexReader.read()
        if(inverted_index_file.strip()):
             indexwriter_changed = open('Merge/invert_index.txt',"w+")
             lst_elements = inverted_index_file.strip().split('\n')
             print('Beforee ===========>')
             #print('lst:::',lst_elements)
             for i in range(len(lst_elements)):
                 _each_val = lst_elements[i].split(' -----------> ')
                 _index_places = compression_word.find(_each_val[0].capitalize())
                 _each_val[0] = _each_val[0].replace(_each_val[0], str(_index_places))
                 lst_elements[i] = _each_val[0] +" -----------> "+_each_val[1]
                
            
             for i in range(len(sorted(lst_elements))):
                 indexwriter_changed.write(lst_elements[i])
                 indexwriter_changed.write ("\n")  
                
        print ("Full dictionary compiled!!!!!!.")
        indexReader.close()
        compression_word_list.close()
        indexwriter_changed.close()















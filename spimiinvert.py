import collections
import sys
import time
import tracemalloc
from collections import OrderedDict

global block_number 
block_number = 0
def spimiinvert(documents,ACTUALFILESIZE):
        print("=============== Applying SPIMI... ===============")
        tracemalloc.start()
        startspimi = time.process_time()
        documents_count = len(documents)
        dictionary = {} # (term - postings list)
        for index, docID in enumerate(documents):
                for term in documents[docID]:
                        if term not in dictionary:
                                dictionary[term] = [int(docID)]
                        else:
                                dictionary[term].append(int(docID))
                if sys.getsizeof(dictionary) > int(ACTUALFILESIZE) or (index == documents_count-1):
                                print(" -- Sorting terms...")
                                sorted_dictionary = OrderedDict() # keep track of insertion order
                                sorted_terms = sorted(dictionary)
                                for term in sorted_terms:
                                        result = [docIds for docIds in dictionary[term]]
                                        counter = collections.Counter(result)
                                        c = [counter[docId] for docId in counter.keys()]
                                        sorted_dictionary[term] = [sum(c),[docId for docId in counter.keys()]]
                                """ Writes index of the block (dictionary + postings list) to disk """
                                # Define block
                                base_path = 'index_blocks/'
                                global block_number
                                block_name = 'block-' + str(block_number) + '.txt'
                                block = open(base_path + block_name, 'a+')
                                print(" -- Writing term-positing list block: " + block_name + "...")
                                # Write term : posting lists to block
                                for index, term in enumerate(sorted_dictionary):
                                        block.write((term.encode('utf-8').decode('ascii', 'ignore'))+" -----------> "+ str(sorted_dictionary[term]) + "\n")
                                block.close()
                                current, peak = tracemalloc.get_traced_memory()
                                print(f" After block : Current memory usage is {current / 10**6}MB")
                                tracemalloc.stop()
                                endspimi = time.process_time()
                                spimitime = endspimi - startspimi
                                print("Time Taken for each SPIMI Block : ", spimitime,"Sec")
                                block_number = block_number + 1
                                dictionary = {}      
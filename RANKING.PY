import os
import FILEOPS22
import _pickle as cPickle
import operator
from math import log10
import collections
from collections import OrderedDict
import json
class SPIMIRanking:	
        def __init__(self):
                    self.index = FILEOPS22.readIndexIntoMemory()
                    self.index1 = FILEOPS22.readRankintomemory()
                    
        def multiple_and_keyword_query(self,query):
                docIds = [] 
                terms =  query.split(' and ')
                for i, term in enumerate(terms):
                        print ("The terms are : ",str((i + 1)) + ": " + term)
                print ("" )
                for term in query.split():
                    #print('The terms are : ',term)
                    if term in self.index1:
                        term_doclist = []
                        for posting in (self.index1[term]):
                                posting_doc = str(posting[0])
                                term_doclist.append(posting_doc)   
                        docIds.append(term_doclist)               
                results = list(set.intersection(*map(set, docIds))) 
                print('Document IDS without Ranking for AND --- : ',results)
                return results        
                                
            
        def multiple_or_keyword_query(self,query):
                docIds = []
                #inverted_index = get_inverted_index(index_file)
                terms =  query.split(' or ')
                for i, term in enumerate(terms):
                        print ("The terms are : ",str((i + 1)) + ": " + term)
                #print ("" )
                for term in query.split():
                    #print('The terms are : ',term)
                    if term in self.index1:
                        term_doclist = []
                        for posting in (self.index1[term]):
                                
                                posting_doc = str(posting[0])
                                term_doclist.append(posting_doc)
                               
                                
                        docIds.append(term_doclist)
                       
               
                results = list(set.union(*map(set, docIds))) 
                print('Document IDS without Ranking for OR --- :',results)
                return results
            
        def single_keyword_query(self,query):
             main_indexdict = self.index1
             doc_list=[]
             if main_indexdict.get(query)!=None:
                 
                 for match in main_indexdict.get(query):
                        print("Document IDS without Ranking",str(match[0]))         
                        doc_list.append(str(match[0]))
                
             return doc_list
        
        def GetRankedResults(self,query):
            
            matches_rank = []
            if ' and' in query.lower():
                matches_rank = self.multiple_and_keyword_query(query)
            elif ' or' in query.lower():
                matches_rank = self.multiple_or_keyword_query(query)
            else:
                matches_rank = self.single_keyword_query(query)
                
            rsvd_dict = {}

            with open("DISK/collection_stats", 'rb') as stats_files:
                N, doc_length_dict, avg_doc_length = cPickle.load(stats_files)
            stats_files.close()

            N = float(N)
          
            for term in query.split():
                #print('term------',term)
                if term in self.index1:
                    dft = float(len(self.index1[term]))
                    for posting in (self.index1[term]):
                        posting_doc = str(posting[0])
                       
                        if posting_doc in matches_rank :
                           
                            rsvd = (( posting[2] * (log10((N/dft)))))
                            rsvd_dict[posting_doc] = rsvd
            return sorted(rsvd_dict.items(), key=operator.itemgetter(1), reverse=True)

        def RankDocuments(self):
                        k1 = 1.2
                        b = 0.75
                        out_file = 'Merge/rank_file.txt'
                        # fetch collection stats
                        with open("DISK/collection_stats", 'rb') as stats_files:
                            N, doc_length_dict, avg_doc_length = cPickle.load(stats_files)
                        stats_files.close()                        
                        doc_length_dict = dict(doc_length_dict)
                        selfindexdict = self.index
                        
                        for term, postings in selfindexdict.items():
                                #print(type(postings))
                                postings = json.loads(postings)
                                for index, post in enumerate(postings):
                                        tftd = post[1]
                                        doc_id = post[0]
                                        doc_id = str(doc_id)
                                        ld = doc_length_dict[doc_id]
                                        post = [post[0], post[1], self.calculate_rsv(avg_doc_length, b, k1, ld, tftd)]
                                        postings[index]=post
                                        
                               
                                selfindexdict[term] = postings
                           
                        #print(' self_post[index]', selfindexdict)
                        with open(out_file, "w+") as output_file:
                            #cPickle.dump(self.index, output_file, -1)
                            output_file.write(json.dumps(selfindexdict))
                        output_file.close()


        def calculate_rsv(self,avg_doc_length, b, k1, ld, tftd):
                            avg_doc_length = float(avg_doc_length)
                            b = float(b)
                            k1 = float(k1)
                            ld = float(ld)
                            tftd = float(tftd)
                            return float(((k1 + 1) * tftd) / (k1 * (((1 - b) + b * (ld / avg_doc_length))) + tftd))


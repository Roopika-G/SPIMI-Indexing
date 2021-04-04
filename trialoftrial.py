import os
import Fileops

class SPIMIQuery:	
        def __init__(self):
                    self.index = Fileops.readIndexIntoMemory()
                    
                    self._total_Set = Fileops.getTotalSet(self.index)
                    #self.compression_word = Fileops.compressedstring()
        def runQuery(self,keyword):
                    # Parse keyword HORSE AND (CAT OR DOG)
                    results = self.parseQuery(keyword)
                    #terms1 = complexquery(keyword)
                    #results = searching(keyword, terms)
                    postlist =[]
                    if ' (' in keyword:
                        print("I AM HERE")
                        lower = keyword.lower()
                        first = lower.split(' (')[0]
                        postlist.append(results)
                        lower = keyword.lower()
                        if 'not (' in lower:
                                        print("INSIDE THE NOT ( COMMAND")
                                        operation = 'NOT'
                                        if postlist: # not empty
                                                if operation == 'OR':
                                                        results2 = list(set.union(*map(set, postlist)))
                                                elif operation == 'SETDIFF':
                                                        results2 = list(set.difference(*map(set, postlist)))
                                                elif operation == 'AND':
                                                        results2 = list(set.intersection(*map(set, postlist)))
                                                elif operation == 'NOT':
                                                        results2 = (self._total_Set.difference(set(postlist[0])))
                                        #results1 = list(set.intersection(*map(set, postlist)))
                                
                                                else:
                                                        results2 = []
                                        else: 
                                                results2 = []
                                        if len(results2) == 0: # not empty
                                                print ("Your search - \" " + keyword + " \" - did not match any documents")
                                        else:
                                                print( "Document Results: ", sorted(results2))
                                        print( "####----------------------------------------------------####\n") 
                        else:

                                terms1 = self.complexquery(keyword)
                                #print(terms1)
                                #listOfPostingsList1 =[]
                                if ' or' in first.lower():
                                        operation = 'OR'
                                elif ' and' in first.lower():
                                        operation = 'AND'
                                elif ' not' in first.lower():
                                        operation = 'SETDIFF'
                                elif terms1:
                                        operation = 'None, it\'s a single word query'
                                else:
                                        operation = 'Nothing input'
		
                                print('\nYour Operation Is: ' + operation)
                                print('\nYour Terms Are:')
                                #for i, term in enumerate(terms1):
                                print (terms1)
                                print ("" )# blank line to skip to next line
                                if terms1 in self.index:
                                        postlist.append(self.index[terms1])
                                if postlist: # not empty
                                        if operation == 'OR':
                                                results1 = list(set.union(*map(set, postlist)))
                                        elif operation == 'SETDIFF':
                                                results1 = list(set.difference(*map(set, postlist)))
                                        elif operation == 'AND':
                                                results1 = list(set.intersection(*map(set, postlist)))
                                        elif operation == 'NOT':
                                                results1 = (self._total_Set.difference(set(postlist)))
                                        #results1 = list(set.intersection(*map(set, postlist)))
                                
                                        else:
                                                results1 = []
                                else: 
                                        results1 = []
                                if len(results1) == 0: # not empty
                                        print ("Your search - \" " + keyword + " \" - did not match any documents")
                                else:
                                        print( "Document Results: ", sorted(results1))
                                print( "####----------------------------------------------------####\n")




        def parseQuery(self,keyword):
                    lower = keyword.lower()
                    if ' (' in lower:
                                #flag = 1
                                #c =[]
                                #first = lower.split(' (')[0]
                                a = lower.split(' (')[1]
                                b = a.split(')')[0] 
                                if ' or ' in b:
                                        operation = 'OR'
                                        term =  b.split(' or ')
                                        a = self.searching(operation,term)
                                        return a

                                elif ' not ' in b:
                                        operation = 'SETDIFF'
                                        term =  b.split(' not ')
                                        a = self.searching(operation,term)
                                        return a
                                elif ' and ' in b:
                                        operation = 'AND'
                                        term =  b.split(' and ')
                                        a = self.searching(operation,term)
                                        return a
                                else:
                                        operation = 'NOT'
                                        term =  b.split('not ')
                                        a = self.searching(operation,term)
                                        return a
                    else:
                                if ' or ' in lower:
                                        operation = 'OR'
                                        term =  lower.split(' or ')
                                        self.searching(operation,term)
                                        print("I am here....but why???")
                                        #return a
                                elif ' not ' in lower:
                                        operation = 'SETDIFF'
                                        term =  lower.split(' not ')
                                        self.searching(operation,term)
                                        #return a
                                elif 'not ' in lower:
                                        operation = 'NOT'
                                        term =  lower.split('not ')
                                        self.searching(operation,term)

                                else:
                                        operation = 'AND'
                                        term =  lower.split(' and ')
                                        self.searching(operation,term)
                                        print("I am here....but why???")
                                        #return a



        def complexquery(self,keyword):
                    lower = keyword.lower()
                    if ' (' in lower:
                                #flag =1
                                #c =[]
                                first = lower.split(' (')[0]
                                print(first)
                                #a = lower.split(' (')[1]
                                #b = a.split(')')[0]
                                if ' or ' in first:
                                        print("this is it " ,first.split(' or')[0])
                                        return first.split(' or')[0]
                                        #print(c)
                                elif ' not ' in first:
                                        return first.split(' not')[0]
                                        #print(c)
                                #elif 'not (' in first:
                                        #return first.split('not')[0]
                                        #print(c)
                                elif ' and ' in first:
                                        print("this is it " ,first.split(' and'))
                                        return first.split(' and')[0]
                                elif ' or' in first:
                                        print("this is it " ,first.split(' or')[0])
                                        return first.split(' or')[0]
                                        #print(c)
                                elif ' not' in first:
                                        return first.split(' not')[0]
                                        #print(c)
                                #elif 'not (' in first:
                                        #return first.split('not')[0]
                                        #print(c)
                                else:
                                        print("this is it " ,first.split(' and'))
                                        return first.split(' and')[0]



        def searching(self,operation, terms):
                   # if ' or ' in keyword.lower():
                               # operation = 'OR'
                    #elif ' and ' in keyword.lower():
                               # operation = 'AND'
                    #elif ' not ' in keyword.lower():
                                #operation = 'SETDIFF'
                    #elif terms:
                                #operation = 'None, it\'s a single word query'
                    #else:
                                #operation = 'Nothing input'
                   # print('terms::',terms)
                    if('' in terms):
                       del terms[0]
                    #print('terms----',terms)
		
                    print('\nYour Operation Is: ' + operation)
                    print('\nYour Terms Are:')
                    for i, term in enumerate(terms):
                                print (str((i + 1)) + ": " + term)
                    print ("" )# blank line to skip to next line
                    listOfPostingsList = [[]]
                    for term in terms:
                                term_with_dot = term + '.'
                                if term in self.index:
                                        listOfPostingsList.append(self.index[term])
                                if term_with_dot in self.index:
                                        if len(listOfPostingsList) != 1:
                                                for item in self.index[term_with_dot]:
                                                            listOfPostingsList[len(listOfPostingsList)-1].append(item)
                                        else:
                                                listOfPostingsList.append(self.index[term_with_dot])
                    del listOfPostingsList[0] # delete the blank array initializer so as not to mess up intersection calculation
                    # find intersections
                    if listOfPostingsList: # not empty
                                if operation == 'OR':
                                        results = list(set.union(*map(set, listOfPostingsList)))
                                elif operation == 'SETDIFF':
                                        results = list(set.difference(*map(set, listOfPostingsList)))
                                elif operation == 'NOT':
                                        results = (self._total_Set.difference(set(listOfPostingsList[0])))
                                        del listOfPostingsList[0]
                                elif len(listOfPostingsList) == len(terms):
                                        results = list(set.intersection(*map(set, listOfPostingsList)))
                                
                                else:
                                        results = []
                    else: 
                                results = []
		            #print( "----------------------------------------------------")
                    if len(results) == 0: # not empty
                                print ("Your search - \" " + terms + " \" - did not match any documents")
                    else:
                                print( "Document Results: ", sorted(results))
                    print( "####----------------------------------------------------####\n")
                    return results


#runQuery(query)

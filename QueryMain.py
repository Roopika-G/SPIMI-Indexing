import sys
import trialoftrial as q

def query():
        query = q.SPIMIQuery()
        while (True): # keep running the program 
                keyword = input("\nPlease enter your query:  \n")
                print("\nYou entered: \"" + keyword + "\"")
                query.runQuery(keyword)
                #print(result)


if __name__ == '__main__':
	#generateindex(int(sys.argv[1]))
	query()
        
import glob
import os
corpus = 'F:/Hassan/BSCS/Semester 6/Information Retrieval/Assignment 1/shortstories/*.txt'
stopwordpath = 'F:/Hassan/BSCS/Semester 6/Information Retrieval/Assignment 1/stopwords.txt'
TextFiles = glob.glob(corpus)
DicWord = {}
positionalIndex = {}
StopWords = []

with open(stopwordpath) as stop:
    for lines in stop:
        for word in lines.split():
            StopWords.append(word)
for name in TextFiles:
    with open(name) as f:
        file = f.readlines()[2:]
        counter = 0
        for lines in file:
            for splitted_word in lines.split():
                for word in splitted_word.split('-'):
                    if word.lower() not in (stopword.lower() for stopword in StopWords):
                        counter = counter + 1
                        cleanWord = word.lower().replace('"',"").replace(',',"").replace('.',"").replace(';',"").replace('!',"").replace('?',"").replace('\'',"").replace(':',"")
                        pos = DicWord.setdefault(cleanWord,{})
                        positionalIndex = pos.setdefault((int(os.path.basename(name).split('.')[0])),[])
                        positionalIndex.append(counter)


print(StopWords)
print(len(DicWord.keys()))
print(DicWord)


def NOTfunc(X):
    tempList = set(range(1,51))
    if type(X) == str:
        temp = DicWord.get(X,[])
        if temp != []:
            Posting = temp.keys()
        else:
            Posting = []

        PostingList = list(Posting)
    else:
        PostingList = X
    Result = list(set(tempList)-set(PostingList))
    return Result

def Intersect(X,Y):

        if type(X) == str:
            temp1 = DicWord.get(X,[])
            if temp1 != []:
                Posting1 = temp1.keys()
            else:
                Posting1 = []
            PostingList1= list(Posting1)
        else:
            PostingList1 = X
        if type(Y) == str:
            temp2 = DicWord.get(Y,[])
            if temp2 != []:
                Posting2 = temp2.keys()
            else:
                Posting2 = []
            PostingList2 = list(Posting2)
        else:
            PostingList2 = Y

        Result = []


        lenP1 = len(PostingList1)
        lenP2 = len(PostingList2)
        i=0
        j=0
        while i != lenP1 and j != lenP2:
          docIDP1 = PostingList1[i]
          docIDP2 = PostingList2[j]
          if docIDP1 == docIDP2:
              Result.append(docIDP1)
              i=i+1
              j=j+1
          elif docIDP1 < docIDP2:
              i=i+1
          else:
              j=j+1
        return Result

def Union(X,Y):
    Result = []
    if type(X) == str:
        temp1 = DicWord.get(X, [])
        if temp1!=[]:
            Posting1 = temp1.keys()
        else:
            Posting1 = []
        PostingList1 = list(Posting1)
    else:
        PostingList1 = X
    if type(Y) == str:
        temp2 = DicWord.get(Y, [])
        if temp2 != []:
            Posting2 = temp2.keys()
        else:
            Posting2 = []
        PostingList2 = list(Posting2)
    else:
        PostingList2 = Y

    if PostingList1 == None:
        return PostingList2
    if PostingList2 == None:
        return PostingList1
    if PostingList1 != None and PostingList2 != None:
        Result = list(set(PostingList1).union(PostingList2))

    return Result

def getProximity(X,Y,K):
    answer = []
    temp1 = DicWord.get(X, [])
    if temp1 != []:
        Posting1 = temp1.keys()
    else:
        Posting1 = []
    PostingList1 = list(Posting1)

    temp2 = DicWord.get(Y, [])
    if temp2 != []:
        Posting2 = temp2.keys()
    else:
        Posting2 = []
    PostingList2 = list(Posting2)

    lenP1 = len(PostingList1)
    lenP2 = len(PostingList2)
    i=0
    j=0
    while i!=lenP1 and j!=lenP2:
        docIDp1 = PostingList1[i]
        docIDp2 = PostingList2[j]

        if docIDp1 == docIDp2:
            tempList = list()
            PosP1 = temp1[docIDp1]
            PosP2 = temp2[docIDp2]
            l=0
            m=0
            while l!=len(PosP1):
                while m!=len(PosP2):
                    if abs(PosP1[l] - PosP2[m]) <= K:
                        tempList.append(PosP2[m])
                    else:
                        if PosP2[m] > PosP1[l]:
                            break
                    m=m+1
                while tempList != [] and abs(tempList[0]-PosP1[l])>K:
                    del tempList[0]
                for ps in tempList:
                    answer.append((docIDp1,PosP1[l],ps))
                l=l+1
            i=i+1
            j=j+1
        else:
            if docIDp1 < docIDp2:
                i=i+1
            else:
                j=j+1
    print(answer)
def ProximityRetrieval():
    Query = 0
    while Query!='1':
        print('Type 1 to exit')
        Query = input('Enter Proximity query: ')
        QueryWords = Query.split()
        index=0
        while index < len(QueryWords)-1:
               X= QueryWords[index].split('/')[0]
               Y= QueryWords[index+1].split('/')[0]
               k= QueryWords[index+1].split('/')[1]
               getProximity(X,Y,int(k))
               index = index +1


    #for index, words in enumerate(QueryWords)
def BooleanRetrieval():
    Query = 0
    while Query != '1':
        print('Type 1 to exit')
        Query = input('Enter Boolean query using ''AND'' ''OR'' ''NOT'' operators:')
        QueryWords = Query.split()
        op_count = 1
        Result = []
        for index, words in enumerate(QueryWords):
            if words == 'AND' or words == 'OR':
                if(op_count>1):
                    previous = Result
                else:
                    previous = QueryWords[index - 1].lower()
                if QueryWords[index + 1] != 'NOT':
                    next = QueryWords[index + 1].lower()
                else:
                    next = NOTfunc(QueryWords[index+2].lower())
                if words=='AND':
                    Result = Intersect(previous,next)
                elif words == 'OR':
                    Result = Union(previous,next)
                else:
                    print('Wrong Query')
                op_count = op_count + 1
            else:
                continue

        print(Result)


print("Hello. Welcome to Boolean Retrieval System.")
choice = -1
while choice != '0':
    print('Select any one of them: ')
    print('1. Boolean Query (AND OR NOT)')
    print('2. Proximity Query (e.g X Y/2)')
    print('0. Exit')
    choice = input('Your choice (0 or 1 or 2): ')
    if choice == '1':
        BooleanRetrieval()
    elif choice == '2':
        ProximityRetrieval()
    elif choice == '0':
        print('Thank you!!')
    else:
        print('Wrong choice !')
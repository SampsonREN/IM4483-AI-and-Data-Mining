
# EE4483/IM4483  Artificial Intelligence and Data Mining


# Source Code


```python
import csv
from itertools import combinations


with open('basket.csv','r') as f:
    reader = csv.reader(f)
    readText = list(reader)

baskets=[]

# trim spaces in the data
for i in readText:
    _ = []
    for j in i:
        _.append(j.strip())
    baskets.append(_)

for basket in baskets:
    basket.sort()

hashTable = {}



items=['Apple','Banana','Coffee','Diaper','Egg','Fish','Ginger','Ham','IceCream','Jam','Ketchup','Lemon','Milk','Nuts','Olive','PeanutButter','Quiche','Rootbeer','Salad','Tea']



def scanSupport(candidateList, minsup):
    frequentList = []
    unfrequentList =[]
    for candidate in candidateList:
        support = 0
        for basket in baskets:
            if isinstance(candidate,str):
                if set([candidate])<=set(basket):
                    support+=1
            else:
                if set(candidate)<=set(basket):
                    support+=1
        if support >= minsup:
            frequentList.append(candidate)
            if isinstance(candidate,str):
                hashTable[candidate]=support
            else:
                hashTable['_'.join(candidate)]=support
        else:
            unfrequentList.append(candidate)
    return frequentList,unfrequentList


def removeUnfrequent(candidates,unfrequentList):
    newItems = []
    for i in candidates:
        ispass = True
        for j in unfrequentList:
            if isinstance(j,str):
                if j in i:
                    ispass = False
            else:
                if set(j)<=set(i):
                    ispass = False
        if ispass:
            newItems.append(i)
    return newItems

def frequentItems(frequntList):
    newItems = []
    for i in items:
        for j in frequntList:
            if i in j:
                newItems.append(i)
                break
    return newItems


```

### 1. How many frequent itemsets have the minimum support of 20%, 10%, 5%, and 3% respectively?


```python
def question_1(percent):
    hashTable.clear()
    minSup = 180*percent/100

    frequent,unfrequent = scanSupport(items,minSup)
    for i in range(2,len(items)+1):
        candidates = [list(x) for x in combinations(frequentItems(frequent),i)]
        newCandidates = removeUnfrequent(candidates,unfrequent)
        frequent,unfrequent = scanSupport(newCandidates,minSup) 
    
    return len(hashTable)

print('There are '+str(question_1(20))+' itemsets that have minimum support of 20%.')
print('There are '+str(question_1(10))+' itemsets that have minimum support of 10%.')
print('There are '+str(question_1(5))+' itemsets that have minimum support of 5%.')
print('There are '+str(question_1(3))+' itemsets that have minimum support of 3%.')
```

    There are 20 itemsets that have minimum support of 20%.
    There are 68 itemsets that have minimum support of 10%.
    There are 268 itemsets that have minimum support of 5%.
    There are 659 itemsets that have minimum support of 3%.


### 2. What are the respective percentages of frequent 3‐itemsets, and 2‐itemsets, with respect to all possible itemsets, which have a minimum support of 3%?

From question 1, we have fond that there are 659 itemsets that have minimum support of 3%.


```python
def question_2(num):
    candidates = [list(x) for x in combinations(items,num)]
    frequent,unfrequent = scanSupport(candidates, 180*3/100)
    return len(frequent)/659

print('For 3-itemsets, the percentage is: '+str(question_2(3)))
print('For 2-itemsets, the percentage is: '+str(question_2(2)))
```

    For 3-itemsets, the percentage is: 0.6433990895295902
    For 2-itemsets, the percentage is: 0.2883156297420334


### 3. How many association rules have a minimum confidence of 50% and a minimum support of 5% and 10%, respectively? Briefly explain how the minimum support affects the strong rules generated.


```python
def complement(subset, fullset):
    return [n for n in fullset if n not in subset]


def question_3(percent,minconf):
    hashRelation ={}
    question_1(percent)
    for k in hashTable:
        key = k.split('_')
        if len(key)>=2:
            for i in range(1,len(key)):
                candidates = [list(x) for x in combinations(key,i)]
                #print(candidates)
                for candidate in candidates:
                    if isinstance(candidate,str):
                        candidateKey = candidate
                    else:
                        candidateKey ='_'.join(candidate)
                    confident = hashTable['_'.join(key)]/hashTable[candidateKey]
                    #print(candidate)
                    #print(confident)
                    if confident >= minconf:
                        hashRelation[candidateKey+' -> '+ '_'.join(complement(candidate,key))] = confident
    return hashRelation

print('There are '+ str(len(question_3(5,0.5)))+ ' association rules that have a minimum confidence of 50% and a minimum support of 5%.')
print('There are '+ str(len(question_3(10,0.5)))+ ' association rules that have a minimum confidence of 50% and a minimum support of 10%.')

```

    There are 117 association rules that have a minimum confidence of 50% and a minimum support of 5%.
    There are 0 association rules that have a minimum confidence of 50% and a minimum support of 10%.


Higher minmum supprt will give more restrctions and become harder to genrate strong rules. With the minimum confidence unchanged, larger the minimum supprot is, lesser the strong rules are.

### 4. List three association rules that have the highest support with 100% confidence?

If minmum support is 2.5% (meaning greater or equal to 5), we have


```python
question_3(2.5,1) # output association rules and corresponding confidence
```




    {'Apple_Egg_Nuts -> Ham': 1.0,
     'Banana_Ham_Salad -> Apple': 1.0,
     'Coffee_Diaper_Ginger -> Egg': 1.0,
     'Coffee_Diaper_Ham -> IceCream': 1.0,
     'Coffee_Egg_Salad -> Apple': 1.0,
     'Diaper_Egg_Milk -> Coffee': 1.0,
     'Egg_Ham_Nuts -> Apple': 1.0,
     'Fish_Ketchup_Tea -> Diaper': 1.0,
     'IceCream_Olive_Tea -> Banana': 1.0}



If minmum support is 3% (meaning greater or equal to 6), we have


```python
question_3(3,1) # output association rules and corresponding confidence
```




    {'Banana_Ham_Salad -> Apple': 1.0, 'IceCream_Olive_Tea -> Banana': 1.0}



If minmum support is 3.5% (meaning greater or equal to 7), we have


```python
question_3(3.5,1) # output association rules and corresponding confidence
```




    {}



Because lager min support will result in lesser rules. Beyond 3.5%, there is no association rules that can have 100% confidence. The three strong rules I obtained are:
* Banana, Ham, Salad -> Apple
* IceCream, Olive, Tea -> Banana
* Apple, Egg, Nuts -> Ham

### 5. Do you find any “interesting” rules? What are they? Briefly explain why.

From question 3 and 4, we can find that it is difficult to have a stong rule which has more than 3% support and more than 50% confidence. 


```python
question_3(5,0.7) #output rules whose support is greater than 5% and confidence is greater than 70%
```




    {'Apple_Egg -> Coffee': 0.7058823529411765,
     'Fish_IceCream -> Banana': 0.8181818181818182,
     'Fish_Tea -> Diaper': 0.7142857142857143,
     'Ham_Salad -> Apple': 0.75}



We can find from the items that most of the items are food and drink, but there is one "Diapper" in this list. And there are some interesting rules related to "Diapper". For example,
* Fish, Tea -> Diapper (Support > 5%, Confidence = 71.4%)
* Fish, Ketchup, Tea -> Diapper (Support > 2.5%, Confidence = 100%)

The lifts of these two are：
* Lift (Fish_Tea, Diaper) = 2.473 (positive correlation)
* Lift (Fish_Ketchup_Tea, Diaper) = 3.463 (positive correlation)

To explain them, a possible explaination is that since "Diapper" is for baby, bady also likes to eat "Ketchup","Tea" is healther than "Coffee", and people believes that "Fish" is also good for baby's health. In other words, a family tends to keep in a good health (drinks tea instead of coffee) when a baby is born. Fish is often regarded as the best food for a baby.


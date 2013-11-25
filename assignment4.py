from __future__ import division
import sys, glob
import collections
from collections import Counter
import numpy

train_file = ('twitter-POS/train.google')
#split by double newline aka by every new tweet
train_file2 = open(train_file).read().split("\n\n")
#split by single newline aka by every word-category-pair
train_list = [i.split('\n') for i in train_file2]
inner = []
outer = []

for x in range(len(train_list)):
  inner = [m.split('\t') for m in train_list[x]]
  outer.append(inner)
train_data = outer

#Caculate the emission probabilities
Caculate_list=[]
#Get the list of [word,POS]
for Data in train_data:
    for data in Data:
        Caculate_list.append(data)

#Count the number of every POS
count=Counter(Pos for word,Pos in Caculate_list[:len(Caculate_list)-1])
POS_list=[]
for entry in count.items():
    POS_list.append(entry[0])

#Count the number of every POS
count=Counter(Pos for word,Pos in Caculate_list[:len(Caculate_list)-1])
#print '+++++++++++++++++++++++++++++++'
#print 'Number of '+POS_list[1], count[POS_list[1]]
#print "++++++++++++++++++++++++++++++++"

#Get the probility of a word to be a POS
Word_POS=[[] for _ in range(len(POS_list))]
for n in range(len(POS_list)):
 for m in range(len(Caculate_list)-1):#something is wrong here, I donot know why
    if Caculate_list[m][1]==POS_list[n]:
     #print Caculate_list
        Word_POS[n].append(Caculate_list[m][0])
# Word_POS represents all categoried words that belong to the sam pag of sentense such as Word_POS[1] reprsents all words that are noun

emission=[]
#print Word_POS[0]
#count_Word_POS=[[] for _ in range(len(POS_list))]
for i in range(len(POS_list)):
  emission.append(Counter( word for word in Word_POS[i]))#Caculate every word's number in Noun word list
#Here count2 is a list of Counters and in each item of Counter is    word:probability
for m in range(len(POS_list)):
 for item in emission[m].items():
      emission[m][item[0]]=item[1]/count[POS_list[m]]


emissiondict={}
emissionDict={}
for i in range(len(POS_list)):
    for item in emission[i].items():
        emissiondict[item[0]]=item[1]
    emissionDict[POS_list[i]]=emissiondict
    emissiondict={}
print emissionDict['ADV']


# Transition probality

transition=numpy.zeros(12*12).reshape((12,12))    

for i in range(len(train_data)):
    for j in range(len(train_data[i])-1):
        for m in range(len(POS_list)):
            for n in range(len(POS_list)):
              if train_data[i][j][1]==POS_list[m] and train_data[i][j+1][1] and train_data[i][j+1][1]==POS_list[n] :
                  transition[m][n]+=1
            
Sum=[]
sum=0
for i in range(len(POS_list)):
    for j in range(len(POS_list)):
      sum+=transition[i][j] 
    Sum.append(sum) 
    sum=0

for i in range(len(POS_list)):
    for j in range(len(POS_list)):
      transition[i][j]=transition[i][j]/Sum[i]
#print transition

transitiondict={}
transitionDict={}
for i in range(len(POS_list)):
    for j in range(len(POS_list)):
        transitiondict[POS_list[j]]=transition[i][j]
    transitionDict[POS_list[i]]=transitiondict
    transitiondict={}
    
print transitionDict

# Start Probality
Start_word=[]
for i in range(len(train_data)-1):
    Start_word.append(train_data[i][0][1])
count_start=Counter(word for word in Start_word)

startdict={}
startDict={}
sum_start=0
for num in count_start.items():
    sum_start+=num[1]
print sum_start
for i in range(len(train_data)):
    for item in count_start.items():
        startdict[item[0]]=item[1]/sum_start

print startdict





from __future__ import division
import sys, glob
import collections
from collections import Counter
import numpy

######################################################
#
#       Opening & preparing our train and test set
#
######################################################

train_file = ('twitter-POS/train.google')
test_file = ('twitter-POS/test.google')
#train_file = ('/Users/Maria/Documents/ITandcognition/bin/twitter-POS/train.google')
#test_file = ('/Users/Maria/Documents/ITandcognition/bin/twitter-POS/test.google')

#split by double newline aka by every new tweet
test_file2 = open(test_file).read().split("\n\n")
train_file2 = open(train_file).read().split("\n\n")

#split by single newline aka by every word-category-pair
train_list = [i.split('\n') for i in train_file2]
test_list = [i.split('\n') for i in test_file2]

def prepare_data(train_list):
#this function returns a list of list of the train data. It has the following structure:
#[[tweet1[word1, pos1],[word2, pos2]...]] [tweet2[word1, pos1]...]...]. 
#converts to lowercase
  inner = []
  outer = []

  for x in range(len(train_list)):
    inner = [m.lower().split('\t') for m in train_list[x]]
    outer.append(inner)
  train_data = outer
  return train_data


####################################################
#
#       The best HMM ever made
#
####################################################

class BestHMM:

  def __init__(self):
    self.name = BestHMM
    self.Calculate_list = [] # a nested list of all words and their adjecent POS [[word1, POS1], [word2, POS2]...]
    self.POS_list= [] # a 1D list of all POS 
    self.Word_POS = [] # Word_POS represents all categorized words that belong to the same POS i.e. Word_POS[1] represents all words that are nouns
    self.Start_word = []


    print '(Initializing %s)' % self.name


  def state_obs(self,test_list):
#what does this do?
    for Data in test_list:
      for data in Data:
        "do nothing"

    states=POS_list
    observations=[]
    for i in range(len(Word_POS)):
        for j in range(len(Word_POS[i])):
           observations.append(Word_POS[i][j])

#---------------------------------------------------------------------------
# Here we begin the probability calculations

  def Em_prob(self,train_data):
    Calculate_list = self.Calculate_list
    POS_list = self.POS_list
  #Caculate the emission probabilities
  #Get the list of [word,POS] out of the nested list that groups each sentence
    for Data in train_data:
        for data in Data:
            self.Calculate_list.append(data)

    #Count the number of every POS and append them to POS_list
    count=Counter(Pos for word,Pos in Calculate_list[:len(Calculate_list)-1]) #Empty list at the end we want to circumvent
    for entry in count.items():
        POS_list.append(entry[0])

    #Get the probility of a word to be a POS
    Word_POS=[[] for _ in range(len(POS_list))]
    for n in range(len(POS_list)):
     for m in range(len(Calculate_list)-1):#Again empty element
        if Calculate_list[m][1]==POS_list[n]:
            Word_POS[n].append(Calculate_list[m][0])
    

    emission=[] # this list will contain a list of counters of words belonging to every POS.
    for i in range(len(POS_list)):
      emission.append(Counter( word for word in Word_POS[i])) #Count number of words belonging to every POS
    
    for m in range(len(POS_list)):
     for item in emission[m].items():
          emission[m][item[0]]=item[1]/count[POS_list[m]]

    
    emissiondict={}
    emissionDict={}
    for i in range(len(POS_list)):
     for words in Calculate_list:
        for word in words:
         if word in emission[i].keys(): 
            emissiondict[word]=emission[i][word]
         else: emissiondict[word]=0.0
     emissionDict[POS_list[i]]=emissiondict
     emissiondict={}

    return emissionDict


  def Tr_prob(self,train_data):
  #this function count how many times a transistion between any POS tags occur. There are 12 different POS. Therefore the transistions are plotted in a 12 by 12 matrix 
    transition=numpy.zeros(12*12).reshape((12,12))    
    Sum=[]
    transitiondict={} #temporary dictionary
    transitionDict={} # a dictionary of dictionaies. Contains probabilities of transistions between all POS
    POS_list = self.POS_list

    for i in range(len(train_data)):
        for j in range(len(train_data[i])-1):
            for m in range(len(POS_list)):
                for n in range(len(POS_list)):
                  if train_data[i][j][1]==POS_list[m] and train_data[i][j+1][1] and train_data[i][j+1][1]==POS_list[n] :
                      transition[m][n]+=1
# The result from transition matrix is plotted in the Sum list
    sum=0
    for i in range(len(POS_list)):
        for j in range(len(POS_list)):
          sum+=transition[i][j] 
        Sum.append(sum) 
        sum=0
# - and every count is divided by the number of times the start POS occurs
    for i in range(len(POS_list)):
        for j in range(len(POS_list)):
          transition[i][j]=transition[i][j]/Sum[i]
# finally added to the transitionsDict 
    for i in range(len(POS_list)):
        for j in range(len(POS_list)):
            transitiondict[POS_list[j]]=transition[i][j]
        transitionDict[POS_list[i]]=transitiondict
        transitiondict={}
        
    return transitionDict


  def St_prob(self,train_data):
# Start probability this function calculates the probability that a POS belongs to the first word of a tweet
    startdict={} # contains the POS and count
    sum_start=0
    Start_word=self.Start_word # a list of all first words of all tweets

    for i in range(len(train_data)-1):
        Start_word.append(train_data[i][0][1])
    count_start=Counter(word for word in Start_word)

    for num in count_start.items():
        sum_start+=num[1]

    for i in range(len(train_data)):
        for item in count_start.items():
            startdict[item[0]]=item[1]/sum_start

    return startdict


#---------------------------------------------------------------------------
# Here we begin to get the viterbi patch

  def print_dptable(self, V):
      print "    ",
      for i in range(len(V)): print "%7s" % ("%d" % i),
      print
   
      for y in V[0].keys():
          print "%.5s: " % y,
          for t in range(len(V)):
              print "%.7s" % ("%f" % V[t][y]),
          print
   
  # visualize viterbi
  def viterbi(self, obs, states, start_p, trans_p, emit_p):
      V = [{}]
      Vlist = []
      Start_word = self.Start_word
      path=[]
      fullpath={}#it's a lie!

      # Initialize base cases (t == 0)
      for y in states:
          tpath = []
          
          if obs[0] in emit_p[y].keys():
            V[0][y] = start_p[y] * emit_p[y][obs[0]]
          else:
            V[0][y] = start_p[y] * 0.0833

          #V[0][y] = max(start_p[y]*0.0833 if not l in emit_p[y].keys() else start_p[y]*emit_p[y][l] for l in obs) - slighty different and worse
          path.append(y)
          fullpath[y] = tpath #We now have a a dict with the start probabilities

      # Run Viterbi for t > 0
      for t in range(1,len(obs)):
          V.append({})
          newpath = {}

          for y in states:
            if obs[t] in emit_p[y].keys(): #Check whether the word exists in our sentences
              (prob,state) = max([(V[t-1][y0]*trans_p[y0][y]*emit_p[y][obs[t]],y0) for y0 in states])
            else:
              (prob,state) = max([(V[t-1][y0]*trans_p[y0][y]*0.0833,y0) for y0 in states]) # We don't know what class unknown words are, therefore they are equally likely 1/12
          
            V[t][y] = prob
            newpath[y] = fullpath[state] + [y]
          fullpath = newpath
   
      #self.print_dptable(V)
      (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
      return (prob, fullpath[state])

  def Fit(self,observations,states):
   return self.viterbi(observations,states,startDict,transitionDict,emissionDict)


  def Score(self, pred, label):
    correct = 0
    labels = []
    for i in range(len(pred)):
      labels.extend(pred[i][1])
    
    print label
    print labels
    for i in range(len(labels)-1): #We're not interested in its confidence level, just its predictions and the last element is empty
        if labels[i] == label[i]: #This should be pretty straightforward!
          correct+=1          
    result = correct / len(label)

    print "acc:\t",result
    return result



###################################################################
#
#                   The calls
#
###################################################################


#-----------------------------------------------------------------
#Creating variables needed for the calls and 
train_data = prepare_data(train_list)
test_data = prepare_data(test_list)

#Here we define our needed variables to create predictions
HMM = BestHMM()
emissionDict = HMM.Em_prob(train_data)
transitionDict = HMM.Tr_prob(train_data)
startDict = HMM.St_prob(train_data)

observations = []
labels = []


#-----------------------------------------------------------------
#Preparing data for our HMM
for elem in test_data:
  sent = []
  for el in elem:
    sent.append(el[0])
    if len(el) == 2:
      labels.append(el[1])

  observations.append(sent)
states = startDict.keys()

#------------------------------------------------------------------
#The ACTUAL calls...
results = []
for sent in observations:
  Fit = HMM.Fit(sent,states) #Somewhat similar to how SKLearn classifiers' .fit(train) works, but we need to store the result instead
  results.append(Fit)
#print Fit #Optional for table / confidence of path + path.. The confidence is quite depressing!

HMM.Score(results,labels)

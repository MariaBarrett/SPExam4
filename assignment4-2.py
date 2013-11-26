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

#train_file = ('twitter-POS/train.google')
#test_file = ('twitter-POS/test.google')
train_file = ('/Users/Maria/Documents/ITandcognition/bin/twitter-POS/train.google')
test_file = ('/Users/Maria/Documents/ITandcognition/bin/twitter-POS/test.google')

#split by double newline aka by every new tweet
test_file2 = open(test_file).read().split("\n\n")
train_file2 = open(train_file).read().split("\n\n")
#split by single newline aka by every word-category-pair
train_list = [i.split('\n') for i in train_file2]
test_list = [i.split('\n') for i in test_file2]


def prepare_data(train_list):
  inner = []
  outer = []

  for x in range(len(train_list)):
    inner = [m.split('\t') for m in train_list[x]]
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
    self.Calculate_list = []
    self.POS_list= []
    self.Word_POS = []

    print '(Initializing %s)' % self.name


  def state_obs(self,test_list):

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
  #Get the list of [word,POS]
    for Data in train_data:
        for data in Data:
            self.Calculate_list.append(data)

    #Count the number of every POS
    count=Counter(Pos for word,Pos in Calculate_list[:len(Calculate_list)-1]) #Empty list at the end we want to circumvent
    for entry in count.items():
        POS_list.append(entry[0])

    #Get the probility of a word to be a POS
    Word_POS=[[] for _ in range(len(POS_list))]
    for n in range(len(POS_list)):
     for m in range(len(Calculate_list)-1):#Again empty element
        if Calculate_list[m][1]==POS_list[n]:
            Word_POS[n].append(Calculate_list[m][0])
    # Word_POS represents all categorized words that belong to the same group of sentences such as Word_POS[1] represents all words that are noun

    emission=[]
    for i in range(len(POS_list)):
      emission.append(Counter( word for word in Word_POS[i]))#Caculate every word's number in Noun word list
    #Here count2 is a list of Counters and in each item of Counter is word:probability
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

    return emissionDict


  def Tr_prob(self,train_data):
    transition=numpy.zeros(12*12).reshape((12,12))    
    Sum=[]
    transitiondict={}
    transitionDict={}
    POS_list = self.POS_list

    for i in range(len(train_data)):
        for j in range(len(train_data[i])-1):
            for m in range(len(POS_list)):
                for n in range(len(POS_list)):
                  if train_data[i][j][1]==POS_list[m] and train_data[i][j+1][1] and train_data[i][j+1][1]==POS_list[n] :
                      transition[m][n]+=1

    sum=0
    for i in range(len(POS_list)):
        for j in range(len(POS_list)):
          sum+=transition[i][j] 
        Sum.append(sum) 
        sum=0

    for i in range(len(POS_list)):
        for j in range(len(POS_list)):
          transition[i][j]=transition[i][j]/Sum[i]

    for i in range(len(POS_list)):
        for j in range(len(POS_list)):
            transitiondict[POS_list[j]]=transition[i][j]
        transitionDict[POS_list[i]]=transitiondict
        transitiondict={}
        
    return transitionDict


  def St_prob(self,train_data):
    startdict={}
    sum_start=0
    Start_word=[]

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
      path = {}
   
      # Initialize base cases (t == 0)
      for y in states:
          V[0][y] = start_p[y]*emit_p[y][obs[0]]
          path[y] = [y]
   
      # Run Viterbi for t > 0
      for t in range(1,len(obs)):
          V.append({})
          newpath = {}
   
          for y in states:
              (prob, state) = max([(V[t-1][y0]*trans_p[y0][y]*emit_p[y][obs[t]], y0) for y0 in states])
              V[t][y] = prob
              newpath[y] = path[state] + [y]
   
          # Don't need to remember the old paths
          path = newpath
   
      print_dptable(V)
      (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
      return (prob, path[state])

  def Prediction(self,observations,states):
   return self.viterbi(observations,states,startDict,transitionDict,emissionDict)



###################################################################
#
#                   The calls
#
###################################################################

train_data = prepare_data(train_list)
test_data = prepare_data(test_list)

#Here we define our needed variables to create predictions
HMM = BestHMM()
emissionDict = HMM.Em_prob(train_data)
transitionDict = HMM.Tr_prob(train_data)
startDict = HMM.St_prob(train_data)

print startDict
print emissionDict

observations = []
for elem in test_data:
  for el in elem:
    observations.append(el[0])

states = startDict.keys()

HMM.Prediction(observations,states)
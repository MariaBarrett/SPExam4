from __future__ import division
from collections import Counter

#########################################################
#
#       Global functions
#
########################################################

def start_probability(data):
#a function which takes data and calculates the start probability 
#i.e. it counts the number of each POS of every first word of every 
#sentence and divide each of them by the number of sentences. 
#It returns a dictionary: The POS is the key and the probability 
# of that POS being assigned to the first word is the value
    numberofsentences = len(data)
    firstword = []
    dict = {}

    for x in data:
        firstword.append(x[0])
    dict = Counter(POS for word, POS in firstword[:len(firstword)-1])
    for entry in dict.items():
        dict[entry[0]] = entry[1] / numberofsentences
    return dict


def state(data):
# a function that returns a list of the different POS-tags aka states. 
    state = []
    for x in data:
        for y in x:
            if len(y) > 1: 
                if y[1] not in state:
                    state.append(y[1])
    return state

###########################################################
#
#       Transition probabilities
#
###########################################################



#########################################################
#
#       Loading in files
#
########################################################

train_file = ('/Users/Maria/Documents/ITandcognition/bin/twitter-POS/train.google')
test_file = ('/Users/Maria/Documents/ITandcognition/bin/twitter-POS/test.google')

#train_file = ('twitter-POS/train.google')
#test_file = ('twitter-POS/test.google')

#split by double newline aka by every new tweet
train_file2 = open(train_file).read().split("\n\n")
test_file2 = open(test_file).read().split("\n\n")

#split by single newline aka by every word-category-pair
train_list = [i.split('\n') for i in train_file2]
test_list = [i.split('\n') for i in test_file2]

#structuring the data as nested lists 
inner = []
outer = []

for x in range(len(train_list)):
    inner = [m.split('\t') for m in train_list[x]]
    outer.append(inner)
train_data = outer

########################################################
#
#       counting...
#
########################################################


#prepare for nltk. I like the way it's done, but suddenly I doubt whether we are going to use it. NLTK does not want the nested list structure, right?
train_data_nltk = [[[x.replace('/','-') for x in l] for l in s] for s in train_data]

print start_probability(train_data)

"""

states = ('pineapple','me','pear')
 
# code modified from wikipedia on hmms

observations = ('me','pe','pe','me')
 
start_probability = {'pineapple': 0.1, 'me': 0.8, 'pear': 0.1} #the number of POS of the first word in each sentence divided by number of tweets
#count number of nouns followed by verbs and divide by total number of nouns
transition_probability = {
   'pineapple' : {'pineapple': 0.0, 'me': 0.7, 'pear': 0.3},
   'me' : {'pineapple': 0.5, 'me': 0.0, 'pear': 0.5},
   'pear' : {'pineapple': 0.3, 'me': 0.7, 'pear': 0.0}
   }
 
emission_probability = { # for every observation: how many times "I" is a noun divide by the number of nouns
   'pineapple' : {'me': 0.1, 'pe': 0.9},
   'me' : {'me': 0.9, 'pe': 0.1},
   'pear' : {'me': 0.3, 'pe': 0.7},
   }

def print_dptable(V):
    print "    ",
    for i in range(len(V)): print "%7s" % ("%d" % i),
    print
 
    for y in V[0].keys():
        print "%.5s: " % y,
        for t in range(len(V)):
            print "%.7s" % ("%f" % V[t][y]),
        print
 
# visualize viterbi
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
 
    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            (prob, state) = max([(V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
        # Don't need to remember the old paths
        path = newpath
 
    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def example():
    return viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)
print example()

"""

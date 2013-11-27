from __future__ import division
from nltk.probability import UniformProbDist
import nltk, sys

############### Functions ##############

def strip(l):
	nl = list([])
	for e in l:
		nl.append(e[0])
	return nl


#train = list(nltk.corpus.TaggedCorpusReader("/home/alex/Documents/ITandCognition/Scientific Programming/SPExam4/twitter-POS",sys.argv[1],sep="/").tagged_sents())
#test = list(nltk.corpus.TaggedCorpusReader("/home/alex/Documents/ITandCognition/Scientific Programming/SPExam4/twitter-POS",sys.argv[2],sep="/").tagged_sents())

train = list(nltk.corpus.TaggedCorpusReader("/Users/Maria/Documents/ITandcognition/bin/twitter-POS",sys.argv[1],sep="/").tagged_sents())
test = list(nltk.corpus.TaggedCorpusReader("/Users/Maria/Documents/ITandcognition/bin/twitter-POS",sys.argv[2],sep="/").tagged_sents())

hmmt  =nltk.tag.HiddenMarkovModelTrainer()
hmm = hmmt.train(labelled_sequences=train)

sys.stderr.write("done training...\n")

(bl,cor,tot) = (0,0,0)

for t in test:
	print hmm.log_probability(t)
	ind = 0
	for e in hmm.tag(strip(t)):
		(word,pred)=e
		gold=t[ind][1]
		tot+=1
		ind+=1
		if pred==gold:
			cor+=1

sys.stderr.write("system:\t"+str(cor/tot)+"\n")
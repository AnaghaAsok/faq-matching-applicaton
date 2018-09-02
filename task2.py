
# coding: utf-8

# In[3]:


import re
import numpy as np
# from nltk.tokenize import token
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import nltk.data
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
def main():
	file=open("corpus.txt","r+")
	corpusFullText=file.read()
	questions=re.findall("\d\)([\w \-']+)?", corpusFullText)
	# print(questions)
	qbow=[]
	answers=[]
	answersbow=[]
	for index,question in enumerate(questions):
		qbow.append(set(question.split(" ")))
		# print(question)
		if index<49:
			regexString=question+"\?([\w\s\d\W]+)[^\d]"+str(index+2)+"\)"
		else:
			regexString=question+"\?([\w\s\d\W]+)"
		answer=re.findall(regexString,corpusFullText)
		# print(answer)
		if (len(answer)>0):
			# print(regexString)
			answerText=answer[0]
			answers.append(answerText)
			answerText=answerText.replace("\n"," ")
			answersbow.append(set(answerText.split(" ")))

	inputSent=input("Enter your query : ")
	topMatchesIndices=calcTopMatches(inputSent,qbow,answersbow)
	print("The top 10 matches for your question are :")
	for i in topMatchesIndices: 
		print(qbow[i])
		print(answersbow[i])
		print(questions[i]+"?")
		print(answers[i])

        
        
        
def calcTopMatches(inputSentence,qbow,answersbow):
	inputBow=set(inputSentence.split(" "))
	scores=[]
	for index,question in enumerate(qbow):
		score=0
		score+=4*len(inputBow.intersection(question))
		score+=len(inputBow.intersection(answersbow[index]))
		scores.append(score)

	# print(scores)
	return np.argsort(scores)[::-1]
main()


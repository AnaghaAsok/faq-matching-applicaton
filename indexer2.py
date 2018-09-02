
# coding: utf-8

# In[1]:


import re
import pysolr
import sys
import nltk
import importlib


feature_vector_file_import = __import__('Project_Part3')
#feature_vector_file_import = importlib.reload('Project_Part3')

solr = pysolr.Solr('http://localhost:8983/solr/nlp_core2')

print("Please wait for the libraries to load and Indexing to start...")

solr.delete(q='*:*')

readFile = open(r"corpus.txt", "r")
textcontent = readFile.read()
questions=re.findall("\d\)([\w \-']+)?", textcontent)
# paragraphs = textcontent.split('\n\n')
#print(len(paragraphs))

sum1 = 0

for index,question in enumerate(questions):

#     paragraph = paragraphs[i].split("\n")
#     articlename = paragraph[0]
#     articletext = "".join(paragraph[1:])

    #    sentences =re.split('\."| \.',articletext)

#     sentences = articletext.split(".")

        article_list = [dict() for x in range(len(questions))]

#     sum1 = sum1 + len(sentences)

#     for j in range(len(sentences)):
        #        print(j)
        article_list[index]["id"] = index
        article_list[index]["name"] = "y"
        article_list[index]["textsentence"] = nltk.word_tokenize(question)
#         sentences[j].split(" ")


        ret = feature_vector_file_import.get_feature_vector(question)
        feature_list = ['POS', 'Lemma', 'Stem', 'Synonym', 'Hypernym', 'Hyponym', 'Meronym', 'Holonym','Headword']
        for f, line in zip(feature_list, ret):
            article_list[index][f] = line

        # print("hi")
        # print(article_list)
        solr.add(article_list)

print("Indexing is complete now...")



# coding: utf-8

# In[2]:


import re
import pysolr
import sys
import nltk
from nltk.corpus import stopwords
import string

#nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from prettytable import PrettyTable

feature_vector_file_import = __import__('Project_Part3')
solr = pysolr.Solr('http://localhost:8983/solr/nlp_core2', timeout=10)

def testsentence():
    testsentence = input("Enter your test sentence: ")
    file=open("corpus.txt","r+")
    corpusFullText=file.read()
    answers=[]
    questions=re.findall("\d\)([\w \-']+)?", corpusFullText)
    for index,question in enumerate(questions):
        if index<49:
            regexString=question+"\?([\w\s\d\W]+)[^\d]"+str(index+2)+"\)"
        else:
            regexString=question+"\?([\w\s\d\W]+)"
        answer=re.findall(regexString,corpusFullText)
        if (len(answer)>0):
            answerText=answer[0]
            answers.append(answerText)

    #print(answers)
    test_article = [dict()]
    # article_list["test"]["id"] = id
    # test_article["test"]["answer"] = iter[1].lower()

    # test_article[0]["textsentence"] = nltk.word_tokenize(testsentence.lower())
    # ret = feature_vector_file_import.get_feature_vector(testsentence.lower())
    stop = stopwords.words('english') + list(string.punctuation)
    testsentencewithoutsw=[i for i in nltk.word_tokenize(testsentence.lower()) if i not in stop]
    test_article[0]["textsentence"] =testsentencewithoutsw
    ret = feature_vector_file_import.get_feature_vector(testsentence)

    feature_list = ['POS', 'Lemma', 'Stem', 'Synonym', 'Hypernym', 'Hyponym', 'Meronym', 'Holonym']
    for f, line in zip(feature_list, ret):
        test_article[0][f] = line

    params_pos = ','.join(test_article[0]["POS"])
    params_lemma = ','.join(test_article[0]["Lemma"])
    params_stem = ','.join(test_article[0]["Stem"])
    params_synonym = ','.join(test_article[0]["Synonym"])
    params_hypernym = ','.join(test_article[0]["Hypernym"])
    params_hyponym = ','.join(test_article[0]["Hyponym"])
    params_meronym = ','.join(test_article[0]["Meronym"])
    params_holonym = ','.join(test_article[0]["Holonym"])
    params_testtokens = ','.join(test_article[0]["textsentence"])
    #params_headword = ','.join(test_article[0]["HeadWord"])

    fq_querystring = 'POS:' + params_pos + ' AND ' + 'Lemma:' + params_lemma + ' AND ' + 'Stem:' + params_stem + ' AND ' + 'Synonym:' + params_synonym + ' AND ' + ' Hypernym:' + params_hypernym + ' AND ' + ' Hyponym:' + params_hyponym + ' AND ' + ' Meronym:' + params_meronym + ' AND ' + ' Holonym:' + params_holonym
    fq_querysubstring = 'POS:' + params_pos + ' AND ' + 'Lemma:' + params_lemma + ' AND ' + 'Stem:' + params_stem + ' AND ' + 'Synonym:' + params_synonym + ' AND ' + ' Hypernym:' + params_hypernym + ' AND ' + ' Hyponym:' + params_hyponym + ' AND ' + ' Meronym:' + params_meronym + ' AND ' + ' Holonym:' + params_holonym
    fq_str = 'textsentence:' + params_testtokens + ' AND ' + fq_querysubstring
    fq_str1 = 'textsentence:' + params_testtokens + ' AND ' + fq_querystring


    #print("\nThe input query for the third task is",'textsentence:' + params_testtokens + fq_querystring)
    print("\nFeature list obtained for the third task is as following: ")
    prettyTbl = PrettyTable(["Feature Names"] + test_article[0]["textsentence"])
    prettyTbl.add_row(["POS Tags"] + test_article[0]["POS"])
    prettyTbl.add_row(["Lemma"] + test_article[0]["Lemma"])
    prettyTbl.add_row(["Stem"] + test_article[0]["Stem"])
    prettyTbl.add_row(["Synonym"] + test_article[0]["Synonym"])
    prettyTbl.add_row(["Hypernym"] + test_article[0]["Hypernym"])
    prettyTbl.add_row(["Hyponym"] + test_article[0]["Hyponym"])
    prettyTbl.add_row(["Meronym"] + test_article[0]["Meronym"])
    prettyTbl.add_row(["Holonym"] + test_article[0]["Holonym"])
    #prettyTbl.add_row(["HeadWord"] + test_article[0]["HeadWord"] + (len(test_article[0]["textsentence"])-1)*["--"])
    print(prettyTbl)

    thirdresults = solr.search(q='textsentence:' + params_testtokens, fq=fq_querystring, start=0, rows=10000)
    print("\nlength of the third task results", len(thirdresults))
    j = 0
    for result in thirdresults:
        if j < 10:
            print("Question is '{:6}'.".format(result['id']), (' '.join(result["textsentence"])))
            print("Question is '{:6}'.".format(answers[int(result['id'])]))
            j += 1

    # combinedresults = solr.search(q=fq_str, start=0, rows=10000)
    #
    # print("\nlength of the combined results", len(combinedresults))
    # k = 0
    # for result in combinedresults:
    #     if k < 10:
    #         print("The text is '{0}'.".format(result['id']), (' '.join(result["textsentence"])))
    #         k += 1

    '''
    headresults = solr.search(q=fq_str1, start=0, rows=10000)

    print("\nlength of the head results", len(headresults), " with HeadWord ", test_article[0]["HeadWord"])
    l = 0
    for result in headresults:
        if l < 10:
            print("The text is '{0}'.".format(result['id']), (' '.join(result["textsentence"])))
            l += 1
    '''
    fq_querysubstring =  'Lemma:' + params_lemma + ' AND ' + 'Stem:' + params_stem
                        # + ' AND ' + 'Synonym:' + params_synonym \
                        # + ' AND ' + ' Hypernym:' + params_hypernym
    # params = {
    #     'defType': 'dismax',
    #     'qf': 'Stem^2 Lemma^4 Synonym^4'
    # }
    # ** params,


    params_boostedlemma = ','.join(test_article[0]["Lemma"])
    params_boostedstem = ','.join(test_article[0]["Stem"])
    params_boostedsynonym = ','.join(test_article[0]["Synonym"])
    params_boostedhypernym = ','.join(test_article[0]["Hypernym"])
    params_boostedtesttokens = ','.join(test_article[0]["textsentence"])
    stem_boost = 4
    lemma_boost = 4
    synonym_boost = 4

    boosted_query_string = '(textsentence:' + params_boostedtesttokens + ')'+ ' AND (Stem:' + params_boostedstem + ')^' + str(stem_boost) + ' AND (Lemma:' + params_boostedlemma + ')^' + str(lemma_boost)                              + ' AND (Synonym:' + params_boostedsynonym + ')^' + str(synonym_boost)
    print("\nThe input query for the fourth task is", boosted_query_string)
    print(boosted_query_string)
    weightedresults = solr.search(q=boosted_query_string,  start=0,rows=10000)
    # weightedresults = solr.search(q='(textsentence:visa,application) AND (Stem: visa,applic)^3 AND (Lemma:visa,application)^3', start=0,rows=10000)
    # weightedresults = solr.search(q='textsentence:' + params_testtokens, fq=fq_querysubstring, start=0, rows=10000)
    print("\nlength of the fourth task results", len(weightedresults), " with weights ")
    l = 0
    for result in weightedresults:
        if l < 10:
            print("Text ID is '{:6}'.".format(result['id']), (' '.join(result["textsentence"])))
            print("Question is '{:6}'.".format(answers[int(result['id'])]))
            l += 1


#final call
testsentence()


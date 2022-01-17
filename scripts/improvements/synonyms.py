# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 15:24:42 2022

@author: diogo
"""

from nltk.corpus import wordnet
import nltk
import pandas


dataset_books = pandas.read_csv("../../dataset/goodreads_books_clean.csv")
#dataset_reviews = pandas.read_csv("../../dataset/goodreads_reviews.csv")

word_dict = {}
words_checked = []


count = 0
for desc in dataset_books["description"]:
    print(count)
    sentences = nltk.sent_tokenize(desc)
    nouns = []
    for sentence in sentences:
     for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
         if word.lower() not in words_checked:
             if (pos == 'NN' or pos == 'NNS'):
                 nouns.append(word.lower())
                 words_checked.append(word.lower())
    for noun in nouns:
        synonyms = []
        for syn in wordnet.synsets(noun):
            for lm in syn.lemmas():
                if lm.name().lower() != noun:
                    synonyms.append(lm.name())#adding into synonyms 
        if len(synonyms) > 1:
            word_dict[noun] = list(set(synonyms))
    count = count +1
    
count = 0
for title in dataset_books["title"]:
    print(count)
    sentences = nltk.sent_tokenize(title)
    nouns = []
    for sentence in sentences:
      for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
          if word.lower() not in words_checked:
              if (pos == 'NN' or pos == 'NNS'):
                  nouns.append(word.lower())
                  words_checked.append(word.lower())
    for noun in nouns:
        synonyms = []
        for syn in wordnet.synsets(noun):
            for lm in syn.lemmas():
                if lm.name().lower() != noun:
                    synonyms.append(lm.name())#adding into synonyms 
        if len(synonyms) > 1:
            word_dict[noun] =  list(set(synonyms))
    count = count +1
    

f = open("synonyms_books.txt", 'w')
    
for k in word_dict.keys():
    list_synonyms = k + " => "
    for value in word_dict[k][:-1]:
        list_synonyms += value + ", " 
    list_synonyms += word_dict[k][-1]
    f.write(list_synonyms + "\n")
    
f.close()
    

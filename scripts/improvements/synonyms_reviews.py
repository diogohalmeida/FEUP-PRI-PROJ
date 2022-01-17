"""
Created on Mon Jan 17 15:24:42 2022

@author: diogo
"""

from nltk.corpus import wordnet
import nltk
import pandas


#dataset_books = pandas.read_csv("../../dataset/goodreads_books_clean.csv")
dataset_reviews = pandas.read_csv("../../dataset/goodreads_reviews.csv")

word_dict = {}
words_checked = []


count = 0
for desc in dataset_reviews[" Reviews"]:
    print(count)
    if not isinstance(desc, str):
        count = count + 1
        continue
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
            word_dict[noun] = set(synonyms)
    count = count +1

f = open("synonyms_reviews.txt", 'w')
    
for k in word_dict.keys():
    matches = list(set([x for x in word_dict[k] if x != k]))
    list_synonyms = k + ", " + ", ".join(matches)
    f.write(list_synonyms + "\n")
    
f.close()
    

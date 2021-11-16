#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 23:06:57 2021

@author: diogo
"""
import pandas
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from re import sub, match
import math
import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language


dataset = pandas.read_csv("../../dataset/goodreads_books_clean.csv")
dataset_reviews = pandas.read_csv("../../dataset/goodreads_reviews.csv")

dataset_awards = pandas.read_csv("../../dataset/awards.csv")
dataset_characters = pandas.read_csv("../../dataset/characters.csv")
dataset_genres = pandas.read_csv("../../dataset/genre_and_votes.csv")

dataset_langs = pandas.read_csv("../../statistics/descriptions_languages.csv")

#Character names word cloud
# text = ""
# for i in dataset_characters['Character']:
#     text = str(i) + " " + text
    
# wordcloud = WordCloud(max_words=200, background_color="white", width=800, height=400).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

# wordcloud.to_file("../../images/plots/wordcloud_characters.png")

#Reviews word cloud
# text = ""
# for i in dataset_reviews[' Reviews']:
#     text = str(i) + " " + text
    
# wordcloud = WordCloud(max_words=200, background_color="white", width=800, height=400).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

# wordcloud.to_file("../../images/plots/wordcloud_reviews.png")

# Book descriptions word cloud
# text = ""
# for i in dataset['description']:
#     text = str(i) + " " + text
    
    
# print("FINISHED")
# wordcloud = WordCloud(max_words=200, background_color="white", width=800, height=400).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

# wordcloud.to_file("../../images/plots/wordcloud_descriptions.png")



#Bar plot of genres with >100.000 votes
# genres_dict = {}
# for column in dataset_genres:
#     if column != "id" and dataset_genres[column].sum() > 100000:
#         genres_dict[column] = dataset_genres[column].sum()
        
# genres_dict_sorted = dict(sorted(genres_dict.items(), key=lambda item: item[1], reverse = True))

# fig = plt.figure(figsize=(16,9))
# ax = fig.add_axes([0,0,1,1])
# ax.bar(genres_dict_sorted.keys(),genres_dict_sorted.values())
# plt.title('Genres with a total of more than 100.000 votes', fontsize=20)
# plt.xlabel('Genres', fontsize=16)
# plt.ylabel('Number of Votes', fontsize=16)
# plt.xticks(rotation=90, fontsize=14)
# plt.yticks(fontsize=14)
# ax.ticklabel_format(style='sci',scilimits=(3,3), axis='y')
# plt.show()



#Bar plot of genres with >1.000 occurences in books
# genres_dict = {}  
# for column in dataset_genres:
#     genre_count = 0
#     if column != "id":
#         for cell in dataset_genres[column]:
#             if cell > 0:
#                 genre_count = genre_count + 1
#     if genre_count > 1000:
#         genres_dict[column] = genre_count
    
# genres_dict_sorted = dict(sorted(genres_dict.items(), key=lambda item: item[1], reverse=True))
    
# fig = plt.figure(figsize=(16,9))
# ax = fig.add_axes([0,0,1,1])
# ax.bar(genres_dict_sorted.keys(),genres_dict_sorted.values())
# plt.title('Genres present in more than 1.000 books', fontsize=20)
# plt.xlabel('Genres', fontsize=16)
# plt.ylabel('Number of Books', fontsize=16)
# plt.xticks(rotation=90, fontsize=14)
# plt.yticks(fontsize=14)
# ax.ticklabel_format(style='plain', axis='y')
# plt.show()
    
   
#Rating distribution histogram
# fig = plt.figure(figsize=(16,9))
# n, bins, patches = plt.hist(dataset['average_rating'], bins=100, facecolor='#2ab0ff', edgecolor='#e0e0e0', linewidth=0.5, alpha=0.7)
# n = n.astype('int') # it MUST be integer
# for i in range(len(patches)):
#     patches[i].set_facecolor(plt.cm.viridis(n[i]/max(n)))
# plt.title('Average Rating Distribution', fontsize=20)
# plt.xlabel('Average Rating', fontsize=16)
# plt.ylabel('Count', fontsize=16)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.show()
    
    
    
#Publish Year distribution histogram
# def parse_year(date):
#     if type(date) == type(float("nan")):
#         return
#     year_check = match(r'.*([1-3][0-9]{3})', date)
#     if year_check != None:
#         return int(year_check.group(1))

# dataset['year_published'] = dataset["date_published"].apply(parse_year)
# fig = plt.figure(figsize=(16,9))
# n, bins, patches = plt.hist(dataset['year_published'].dropna(inplace=False), bins=250, facecolor='#2ab0ff', edgecolor='#e0e0e0', linewidth=0.5, alpha=0.7)
# n = n.astype('int') # it MUST be integer
# for i in range(len(patches)):
#     patches[i].set_facecolor(plt.cm.viridis(n[i]/max(n)))

# plt.title('Publication Year Distribution', fontsize=20)
# plt.xlabel('Year', fontsize=16)
# plt.ylabel('Count', fontsize=16)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.show()   
    

#Book language detection
#Generate language CSV
# def get_lang_detector(nlp, name):
#     return LanguageDetector()


# nlp = spacy.load("en_core_web_sm")
# nlp.max_length = 10000000 # or higher
# Language.factory("language_detector_reviews_2", func= get_lang_detector)
# nlp.add_pipe('language_detector_reviews_2', last=True)


# dataset_languages = pandas.DataFrame(dataset["id"])
# languages = []
# for desc in dataset["description"]:
#     doc = nlp(desc)
#     # document level language detection. Think of it like average language of the document!
#     # sentence level language detection
#     print(doc, doc._.language)
#     languages.append(doc._.language['language'])
        
        
# dataset_languages["language"] = languages
        
# dataset_languages.to_csv('../../statistics/descriptions_languages.csv', index = False)
        
#Generate graph (read from previous csv to )

lang_dict = dataset_langs["language"].value_counts().to_dict()

fig = plt.figure(figsize=(16,9))
ax = fig.add_axes([0,0,1,1])
ax.bar(lang_dict.keys(), lang_dict.values())
plt.title('Description language', fontsize=20)
plt.xlabel('Languages', fontsize=16)
plt.ylabel('Number of Books', fontsize=16)
plt.xticks(rotation=90, fontsize=14)
plt.yticks(fontsize=14)
ax.ticklabel_format(style='plain', axis='y')
ax.set_yscale('log')
plt.show()
    
    
    
    
    
    
    
    
    
    
    
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
import random
from spacy_langdetect import LanguageDetector
from spacy.language import Language
from collections import Counter



dataset = pandas.read_csv("../../dataset/goodreads_books_clean.csv")
dataset_reviews = pandas.read_csv("../../dataset/goodreads_reviews.csv")

dataset_awards = pandas.read_csv("../../dataset/awards.csv")
dataset_characters = pandas.read_csv("../../dataset/characters.csv")
dataset_genres = pandas.read_csv("../../dataset/genre_and_votes.csv")

dataset_langs = pandas.read_csv("../../statistics/descriptions_languages.csv")

#colors (viridis)
colors = ['#440154ff','#481567ff','#482677ff','#453781ff','#404788ff', '#39568cff', '#33638dff', '#2d708eff','#287d8eff','#238a8dff','#1f968bff','#20a387ff','#29af7fff','#3cbb75ff','#55c667ff','#73d055ff','#95d840ff','#b8de29ff','#dce319ff','#fde725ff']


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
# ax.bar(genres_dict_sorted.keys(),genres_dict_sorted.values(), color = "#1f968bff")
# plt.title('Genres with a total of more than 100.000 votes', fontsize=20)
# plt.xlabel('Genres', fontsize=16)
# plt.ylabel('Number of Votes', fontsize=16)
# plt.xticks(rotation=90, fontsize=14)
# plt.yticks(fontsize=14)
# ax.ticklabel_format(style='sci',scilimits=(3,3), axis='y')
# plt.show()



#Bar plot of genres with >1.000 occurences in books
genres_dict = {}  
for column in dataset_genres:
    genre_count = 0
    if column != "id":
        for cell in dataset_genres[column]:
            if cell > 0:
                genre_count = genre_count + 1
    if genre_count > 1000:
        genres_dict[column] = genre_count
    
genres_dict_sorted = dict(sorted(genres_dict.items(), key=lambda item: item[1], reverse=True))
    
fig = plt.figure(figsize=(16,9))
ax = fig.add_axes([0,0,1,1])
ax.bar(genres_dict_sorted.keys(),genres_dict_sorted.values(), color = "#1f968bff")
plt.title('Genres present in more than 1.000 books', fontsize=20)
plt.xlabel('Genres', fontsize=16)
plt.ylabel('Number of Books', fontsize=16)
plt.xticks(rotation=90, fontsize=14)
plt.yticks(fontsize=14)
ax.ticklabel_format(style='plain', axis='y')
plt.show()
    
   
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
    
    
    
#Publication Year distribution histogram
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
# plt.xlim([1850, 2022])
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
# lang_dict = dataset_langs["language"].value_counts().to_dict()

# fig = plt.figure(figsize=(16,9))
# ax = fig.add_axes([0,0,1,1])
# ax.bar(lang_dict.keys(), lang_dict.values(), color = "#1f968bff")
# plt.title('Description language', fontsize=20)
# plt.xlabel('Languages', fontsize=16)
# plt.ylabel('Number of Books', fontsize=16)
# plt.xticks(rotation=90, fontsize=14)
# plt.yticks(fontsize=14)
# ax.ticklabel_format(style='plain', axis='y')
# ax.set_yscale('log')
# plt.show()
    

#Award Year distribution histogram
# fig = plt.figure(figsize=(16,9))
# n, bins, patches = plt.hist(dataset_awards['Year'].dropna(inplace=False), bins=250, facecolor='#2ab0ff', edgecolor='#e0e0e0', linewidth=0.5, alpha=0.7)
# n = n.astype('int') # it MUST be integer
# for i in range(len(patches)):
#     patches[i].set_facecolor(plt.cm.viridis(n[i]/max(n)))

# plt.title('Award Year Distribution', fontsize=20)
# plt.xlabel('Year', fontsize=16)
# plt.ylabel('Count', fontsize=16)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.xlim([1850, 2021])
# plt.show() 


#Author's number of books
# author_books_dict = {'With 1 book':0, 'With 2 books':0, 'With 3 books':0, 'With 4 books':0, 'With >=5 books':0}
# for i in dataset["author"].value_counts().tolist():
#     if i == 1:
#         author_books_dict['With 1 book'] = author_books_dict['With 1 book'] + 1
#         continue
#     if i == 2:
#         author_books_dict['With 2 books'] = author_books_dict['With 2 books'] + 1
#         continue
#     if i == 3:
#         author_books_dict['With 3 books'] = author_books_dict['With 3 books'] + 1
#         continue
#     if i == 4:
#         author_books_dict['With 4 books'] = author_books_dict['With 4 books'] + 1
#         continue
#     if i >= 5:
#         author_books_dict['With >=5 books'] = author_books_dict['With >=5 books'] + 1
#         continue
    
# colors_pie = ['#b8de29ff','#73d055ff','#1f968bff','#39568cff','#440154ff']
# fig1, ax = plt.subplots(figsize=(16,9))
# centre_circle = plt.Circle((0,0),0.70,fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)
# plt.title('Authors by Number of Books', fontsize=20)
# ax.pie(author_books_dict.values(), colors = colors_pie, autopct='%1.1f%%', startangle=90)
# ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# ax.legend().set_visible(False)
# plt.legend(labels=author_books_dict.keys())
# plt.show()    


#Reviews text size

# reviews_text = dataset_reviews[" Reviews"].tolist()
# reviews_words =  []
# for i in reviews_text:
#     reviews_words.append(len(str(i).split(" ")))
    
# reviews_length_dict = {"X-Small (1-49)": 0, "Small (50-99)": 0, "Medium (100-249)": 0, "Large (250-499)":0, "X-Large (500-999)":0, "XX-Large (>1000)":0}
# for i in reviews_words:
#     if i > 0 and i < 50:
#         reviews_length_dict["X-Small (1-49)"] = reviews_length_dict["X-Small (1-49)"] + 1
#         continue
#     if i >= 50 and i < 100:
#         reviews_length_dict["Small (50-99)"] = reviews_length_dict["Small (50-99)"] + 1
#         continue
#     if i >= 100 and i < 250:
#         reviews_length_dict["Medium (100-249)"] = reviews_length_dict["Medium (100-249)"] + 1
#         continue
#     if i >= 250 and i < 500: 
#         reviews_length_dict["Large (250-499)"] = reviews_length_dict["Large (250-499)"] + 1
#         continue
#     if i >= 500 and i < 1000: 
#         reviews_length_dict["X-Large (500-999)"] = reviews_length_dict["X-Large (500-999)"] + 1
#         continue
#     if i >= 1000:
#         reviews_length_dict["XX-Large (>1000)"] = reviews_length_dict["XX-Large (>1000)"] + 1
#         continue
    
# colors_pie = ['#fde725ff','#b8de29ff','#73d055ff','#1f968bff','#39568cff','#440154ff']
# fig1, ax = plt.subplots(figsize=(16,9))
# centre_circle = plt.Circle((0,0),0.70,fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)
# plt.title('Reviews Text Length (in words)', fontsize=20)
# ax.pie(reviews_length_dict.values(), colors = colors_pie, autopct='%1.1f%%', startangle=90)
# ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# ax.legend().set_visible(False)
# plt.legend(labels=reviews_length_dict.keys())
# plt.show()    


#Number of books in a series

# books_series_dict ={"With 1 book":0,"With 2 books":0,"With 3 books":0,"With 4 books":0, "With >=5 books":0}
# series = dataset["series"].dropna().tolist()
# series_split = []
# for i in series:
#     if '#' in i:
#         series_split.append(i.split('#')[0][1:].rstrip())
#     else:
#         series_split.append(i[1:-1].rstrip())

# series_counter = Counter(series_split)
# for i in series_counter.values():
#     if i == 1:
#         books_series_dict["With 1 book"] = books_series_dict["With 1 book"] +1
#         continue
#     if i == 2:
#         books_series_dict["With 2 books"] = books_series_dict["With 2 books"] +1
#         continue
#     if i == 3:
#         books_series_dict["With 3 books"] = books_series_dict["With 3 books"] +1
#         continue
#     if i == 4:
#         books_series_dict["With 4 books"] = books_series_dict["With 4 books"] +1
#         continue
#     if i >= 5:
#         books_series_dict["With >=5 books"] = books_series_dict["With >=5 books"] +1
#         continue
    
# colors_pie = ['#b8de29ff','#73d055ff','#1f968bff','#39568cff','#440154ff']
# fig1, ax = plt.subplots(figsize=(16,9))
# centre_circle = plt.Circle((0,0),0.70,fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)
# plt.title('Series by Number of Books', fontsize=20)
# ax.pie(books_series_dict.values(), colors = colors_pie, autopct='%1.1f%%', startangle=90)
# ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# ax.legend().set_visible(False)
# plt.legend(labels=books_series_dict.keys())
# plt.show()  



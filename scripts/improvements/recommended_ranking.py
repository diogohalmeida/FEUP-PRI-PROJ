# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 20:33:13 2022

@author: diogo
"""

import pandas

dataset = pandas.read_csv("../../dataset/goodreads_books_clean.csv")


dataset["times_recommended"] = 0

for i in dataset["recommended_books"]:
    if not isinstance(i, float):
        ids = i.split(",")
        for id in ids:
            a = dataset.loc[dataset['id'] == int(id)]
            dataset.loc[dataset['id'] == int(id), "times_recommended"] = dataset.loc[dataset['id'] == int(id)]["times_recommended"] + 1
    
 
dataset.to_csv('../../dataset/goodreads_books_clean_ranked.csv', index= False)
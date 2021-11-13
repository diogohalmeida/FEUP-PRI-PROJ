#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 23:06:57 2021

@author: diogo
"""
import pandas

dataset = pandas.read_csv("../../dataset/goodreads_books_clean.csv")
dataset_reviews = pandas.read_csv("../../dataset/goodreads_reviews.csv")

dataset_characters = pandas.read_csv("../../dataset/characters.csv")
dataset_genres = pandas.read_csv("../../dataset/genre_and_votes.csv")

s = dataset_reviews['Id'].unique()

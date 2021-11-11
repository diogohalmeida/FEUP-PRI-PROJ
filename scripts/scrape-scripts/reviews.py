# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 11:52:31 2021

@author: pedro
"""
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from timeit import default_timer
import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from queue import Empty, Queue
import signal
import sys


START_TIME = default_timer()
CLEANR = re.compile('<.*?>')

queue = Queue()

f = open("../dataset/reviews_missing.csv", "w")

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    f.flush()
    f.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def consume():
    f.write('Id, Reviews, Users, Dates' + '\n')
    while True:
        if not queue.empty():
            bookId, rows = queue.get()
            # Row comes out of queue; CSV writing goes here
            for row in rows:
                f.write(row)


def parseGenres(bookId, data):
    soup = BeautifulSoup(data, "html.parser")
    genresList = soup.find("ul", class_="CollapsableList")
    soup = BeautifulSoup(str(genresList), "html.parser")
    genres = soup.find_all("span", class_="Button__labelItem")

    genres_final = []
    for genre in genres:
        gg = re.findall('(?<=<span class="Button__labelItem">).+?(?=<\/span>)',str(genre))
        if gg and not re.search('[0-9-.]', gg[0]) and re.search('(?=.*[A-Z])', gg[0]): #match genres without numbers chars and with uppercase letters
            genres_final.append(gg[0])
    if not genres_final:
        return bookId, []
    return bookId, [str(bookId) + ',' + '\"' + ','.join(genres_final) + '\"' + '\n']


def parseReviews(bookId, data):
    soup = BeautifulSoup(data, "html.parser")
    reviews = soup.find_all("div", class_="ReviewsList")
    soup = BeautifulSoup(str(reviews[0]), "html.parser")
    reviews = soup.find_all("span", class_="Formatted")
    users = soup.find_all("div", class_="ReviewerProfile__name")
    dates = soup.find_all("span", class_="Text Text__body3")
    index = 0

    csv_reviews = []

    for review in reviews:
        rr = re.findall('(?<=<span class="Formatted">).+?(?=<\/span>)',str(review))
        if rr and re.match('.[a-zA-Z0-9-()]', rr[0]):
            name = users[index].findChildren("a" , recursive=False)
            date = dates[index].findChildren("a" , recursive=False)
            r = CLEANR.sub('', rr[0])
            csv_reviews.append(str(bookId) + ',' + '\"' + str(r).replace('\"', '\'') + '\"' + ',' + '\"' + name[0].text + '\"' + ',' + '\"' + date[0].text + '\"' + '\n')
        index = index + 1
    return bookId, csv_reviews


def fetch(session, bookId):
    #if bookId > 763255: #remove comment if script breaks for some reason -> continue on specified id

    base_url = 'https://www.goodreads.com/book/show/'

    with session.get(base_url + str(bookId)) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::" + base_url + str(bookId))

        #select genres or reviews - comment/uncomment

        queue.put(parseReviews(bookId,data))
        #queue.put(parseGenres(bookId,data))

        elapsed = default_timer() - START_TIME
        time_completed_at = "{:5.2f}s".format(elapsed)
        print("{0:<30} {1:>20}".format(bookId, time_completed_at))

        return


async def get_data_asynchronous(bookIds_to_fetch):
    print("{0:<30} {1:>20}".format("Book", "Completed at"))

    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            
            # Set any session parameters here before calling `fetch`
            session.cookies.set("srb_1", "1_wl")

            # Initialize the event loop        
            loop = asyncio.get_event_loop()

            # Set the START_TIME for the `fetch` function
            START_TIME = default_timer()

            # Use list comprehension to create a list of
            # tasks to complete. The executor will run the `fetch`
            # function for each csv in the csvs_to_fetch list
            
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, row.name) # Allows us to pass in multiple arguments to `fetch`
                )
                for index, row in bookIds_to_fetch.iterrows()
            ]

            # Initializes the tasks to run and awaits their results
            

consumer = Thread(target=consume)
consumer.setDaemon(True)
consumer.start()

def main(): 
    col_list = ["id"]

    #input file to get ids
    bookIds_to_fetch = pd.read_csv("../dataset/missing.csv", index_col=0, usecols=col_list)
    
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(bookIds_to_fetch))
    loop.run_until_complete(future)

    consumer.join()


main()

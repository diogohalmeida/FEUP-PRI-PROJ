import pandas
import re

dataset = pandas.read_csv("../../dataset/goodreads_books_clean.csv")
ids = dataset["id"].tolist()

awards = dataset["awards"]

awards_list = []

for id, row in dataset.iterrows():
    if type(row['awards']) != type(float('nan')):
        awards_aux = [" ".join(j.split(",")) for j in row['awards'].split(";")]            
        aux1 = []        
        for j in awards_aux:
            aux2 = re.split('(?<=\d\))[ ]+(?=[A-Z])', j)
            for i in aux2:
                awards_list.append((row['id'], i))
                
                
awards_frame = pandas.DataFrame(awards_list,columns=["id","Award"])

awards_frame.to_csv('../../dataset/awards.csv', index = False)
            
                
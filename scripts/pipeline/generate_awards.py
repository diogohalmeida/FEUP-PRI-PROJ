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

years = []

year_regex = re.compile(r'\d\d\d\d')


for id, row in awards_frame.iterrows():
    award = row['Award']
    year = year_regex.search(award)
    award_without_year = re.sub('\(\d\d\d\d\)', '' , award)
    awards_frame['Award'].replace(row['Award'], award_without_year, inplace=True)
    if year != None:
        years.append(year.group())
    else:
        years.append(None)
        
awards_frame["Year"] = years

awards_frame.to_csv('../../dataset/awards.csv', index = False)
            
                
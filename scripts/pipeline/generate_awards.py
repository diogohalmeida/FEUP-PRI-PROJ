import pandas

dataset = pandas.read_csv("../../dataset/clean_data.csv")
ids = dataset["id"].tolist()

awards1 = dataset["awards"]

def populate_genre_cols(books, genre):
    book_awards = books["awards"]
    if type(book_awards) == type(float('nan')):
        return None
    genre_list = book_awards.split(",")
    for i in genre_list:
        if genre == " ".join(i.split()[:-1]):
            return int(i.split()[-1].replace("user", ""))
    return None


award_count = {}
aux = []

for id, row in dataset.iterrows():
    if type(row['awards']) != type(float('nan')):
        awards = [" ".join(j.split(",")) for j in row['awards'].split(";")]
        aux1 = " "
        for j in awards:
            aux1.join(j.split("  "))
        for i in aux:
            if i not in award_count.keys():
                award_count[i] = 1
            else:
                award_count[i] += 1
                
# awards_to_use = set()

# for k, v in award_count.items():
#     # if v >= 1000:
#     awards_to_use.add(k)
    
# data = {'id': ids}

# awards_data_frame = pandas.DataFrame(data)


# for i in awards_to_use:
#     awards_data_frame[i.lower().replace(" ", "_")] = dataset.apply(populate_genre_cols, genre=i, axis=1)
    
# awards_data_frame.fillna(0, inplace=True)

# awards_data_frame.to_csv('../../dataset/genre_and_votes.csv', index = False)
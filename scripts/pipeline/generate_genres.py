import pandas

dataset = pandas.read_csv("../../dataset/goodreads_books_clean.csv")
ids = dataset["id"].tolist()

def populate_genre_cols(books, genre):
    book_genres = books["genre_and_votes"]
    if type(book_genres) == type(float('nan')):
        return None
    genre_list = book_genres.split(",")
    for i in genre_list:
        if genre == " ".join(i.split()[:-1]):
            return int(i.split()[-1].replace("user", ""))
    return None
        
genre_count = {}

for id, row in dataset.iterrows():
    if type(row['genre_and_votes']) != type(float('nan')):
        book_genres = [" ".join(j.split()[:-1]) for j in row['genre_and_votes'].split(",")]
        for j in book_genres:
            if j not in genre_count.keys():
                genre_count[j] = 1
            else:
                genre_count[j] += 1
                
genres_to_use = set()

for k, v in genre_count.items():
    # if v >= 1000:
    genres_to_use.add(k)
    
data = {'id': ids}

genres_data_frame = pandas.DataFrame(data)


for i in genres_to_use:
    genres_data_frame[i.lower().replace(" ", "_")] = dataset.apply(populate_genre_cols, genre=i, axis=1)
    
genres_data_frame.fillna(0, inplace=True)

genres_data_frame.to_csv('../../dataset/genre_and_votes.csv', index = False)
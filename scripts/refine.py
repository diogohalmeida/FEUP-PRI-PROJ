import pandas

dataset = pandas.read_csv("../dataset/goodreads_books.csv")

print(len(dataset))


dataset.dropna(subset=['title', 'link', 'cover_link', 'author', 'author_link', 'rating_count', 'average_rating', 'five_star_ratings',
                           'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings',
                           'number_of_pages', 'date_published', 'publisher', 'genre_and_votes','isbn','isbn13', 'amazon_redirect_link',
                           'worldcat_redirect_link', 'description'], inplace=True)

#Remove useless column
dataset.drop(columns=['asin', 'review_count'], inplace=True)

dataset = dataset[dataset.title.str.contains('.[a-zA-Z0-9-()]', regex= True, na=False)]

#All book ids (useful to remove associated books that have been removed)
ids = dataset["id"].tolist()

to_delete = list()  # this will speed things up doing only 1 delete
for id, row in dataset.iterrows():
    if(not pandas.isnull(row.books_in_series)):
        series_ids = [int(s) for s in str(row.books_in_series).split(',')]
        for serie_id in series_ids:
            if(serie_id not in ids):
                series_ids.remove(serie_id)
        row["books_in_series"] = series_ids
            

#to_delete = list()  # this will speed things up doing only 1 delete
for id, row in dataset.iterrows():
    if(not pandas.isnull(row.recommended_books)):
        series_ids = [int(s) for s in str(row.recommended_books).split(',')]
        for serie_id in series_ids:
              if(serie_id not in ids):
                  series_ids.remove(serie_id)
        row["recommended_books"] = series_ids


dataset.to_csv('../dataset/clean_data.csv', index = False)

#TO DO - Remove recommended/books in series that don't exist in the dataset

print(len(dataset))

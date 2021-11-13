import pandas

dataset = pandas.read_csv("../../dataset/goodreads_books.csv")
dataset_reviews = pandas.read_csv("../../dataset/goodreads_reviews.csv")

print(len(dataset))

dataset.dropna(subset=['title', 'link', 'cover_link', 'author', 'author_link', 'rating_count', 'average_rating', 'five_star_ratings',
                           'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings',
                           'number_of_pages', 'date_published', 'publisher', 'genre_and_votes','isbn','isbn13', 'amazon_redirect_link',
                           'worldcat_redirect_link', 'description'], inplace=True)




print(len(dataset))
dataset = dataset[dataset['description'].map(len) >= 100]
print(len(dataset))
#Remove useless column
dataset.drop(columns=['asin', 'review_count'], inplace=True)

#Remove books that have strange chars
dataset = dataset[dataset.title.str.contains('.[a-zA-Z0-9-()]', regex= True, na=False)]
dataset = dataset[dataset.description.str.contains('.[a-zA-Z0-9-()]', regex= True, na=False)]

#All book ids (useful to remove associated books that have been removed)
ids = dataset["id"].tolist()


#Delete books from original dataset that are not in the review dataset
ids_review = dataset_reviews["Id"].unique().tolist()
missing = list(set(ids) - set(ids_review))
dataset = dataset[~dataset.id.isin(missing)]

print(len(dataset))

#Delete books from recommended and series cells that were removed before
# to_delete = list()  # this will speed things up doing only 1 delete
# for id, row in dataset.iterrows():
#     if(not pandas.isnull(row.books_in_series)):
#         series_ids = [int(s) for s in str(row.books_in_series).split(',')]
#         for serie_id in series_ids:
#             if(serie_id not in ids):
#                 series_ids.remove(serie_id)
#         row["books_in_series"] = series_ids
            

# #to_delete = list()  # this will speed things up doing only 1 delete
# for id, row in dataset.iterrows():
#     if(not pandas.isnull(row.recommended_books)):
#         series_ids = [int(s) for s in str(row.recommended_books).split(',')]
#         for serie_id in series_ids:
#               if(serie_id not in ids):
#                   series_ids.remove(serie_id)
#         row["recommended_books"] = series_ids


# dataset.to_csv('../../dataset/teste.csv', index = False)

print(len(dataset))

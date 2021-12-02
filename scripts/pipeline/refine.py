import pandas


def fix_encoding(text):
    if isinstance(text, str):
        return text.encode('latin-1', 'ignore').decode('utf-8', 'ignore')
    

dataset = pandas.read_csv("../../dataset/goodreads_books.csv")

dataset_reviews = pandas.read_csv("../../dataset/goodreads_reviews.csv")

print("Initial: " + str(len(dataset)))

#Remove useless column
dataset.drop(columns=['asin', 'review_count'], inplace=True)

#Add title if book doesn't have an original title
for i in dataset.index:
    if not isinstance(dataset.iloc[i]['original_title'], str):
        dataset.at[i, 'original_title'] = dataset.iloc[i]['title']


#Drop rows with NaN values in the following columns:
dataset.dropna(subset=['title', 'link', 'cover_link', 'author', 'author_link', 'rating_count', 'average_rating', 'five_star_ratings',
                           'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings',
                           'number_of_pages', 'date_published', 'publisher', 'genre_and_votes','isbn','isbn13', 'amazon_redirect_link',
                           'worldcat_redirect_link', 'description'], inplace=True)


print("After NaN drop: " + str(len(dataset)))

#Fix encoding
dataset['title'] = dataset['title'].map(lambda x: fix_encoding(x))
dataset['series'] = dataset['series'].map(lambda x: fix_encoding(x))
dataset['author'] = dataset['author'].map(lambda x: fix_encoding(x))
dataset['publisher'] = dataset['publisher'].map(lambda x: fix_encoding(x))
dataset['original_title'] = dataset['original_title'].map(lambda x: fix_encoding(x))
dataset['settings'] = dataset['settings'].map(lambda x: fix_encoding(x))
dataset['characters'] = dataset['characters'].map(lambda x: fix_encoding(x))
dataset['awards'] = dataset['awards'].map(lambda x: fix_encoding(x))
dataset['description'] = dataset['description'].map(lambda x: fix_encoding(x))

#Remove descriptions with less that 25 characters
dataset = dataset[dataset['description'].map(len) >= 25]
print("After removing short descriptions: " + str(len(dataset)))


#Delete books from original dataset that are not in the review dataset
ids = dataset["id"].tolist()
ids_review = dataset_reviews["Id"].unique().tolist()
missing = list(set(ids) - set(ids_review))
dataset = dataset[~dataset.id.isin(missing)]

print("After removing books that are not in review dataset: " + str(len(dataset)))

#Fix ISBN (make it a string)
dataset["isbn"] = dataset["isbn"].map(str)

# genre_and_votes_list = []
# for i in dataset["genre_and_votes"].tolist():
#     genre_and_votes_list.append(i.split(","))

# dataset["genre_and_votes"] = genre_and_votes_list


# # #Delete books from recommended and series cells that were removed before
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


dataset.to_json('../../dataset/goodreads_books_clean.json', orient="records")

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

dataset["number_of_pages"] = dataset["number_of_pages"].map(int)

# genre_and_votes_list = []
# for i in dataset["genre_and_votes"].tolist():
#     genre_and_votes_list.append(i.split(","))

# dataset["genre_and_votes"] = genre_and_votes_list

ids = dataset["id"].tolist()
#Delete books from recommended and series cells that were removed before

def remove_ids(available_ids, ids_string):
    if pandas.isnull(ids_string):
        return ""
    ids_list = ids_string.split(',')
    ids_list = list(set(map(int, ids_list)))
    final_list = []
    for i in ids_list:
        if i in available_ids:
            final_list.append(i)
    str_list = [str(i) for i in final_list]
    return ",".join(str_list)
    

dataset['recommended_books'] = dataset['recommended_books'].apply(lambda x: remove_ids(ids, x))
dataset['books_in_series'] = dataset['books_in_series'].apply(lambda x: remove_ids(ids, x))


dataset.to_csv('../../solr/goodreads_books_clean.csv', index= False)
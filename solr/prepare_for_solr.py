import pandas 

def replace_id_by_title(dictionary, ids_string):
    titles_str = ""
    if pandas.isnull(ids_string):
        return titles_str
    
    ids_list = ids_string.split(',')
    ids_list = list(map(int, ids_list))
    for i in ids_list:
        titles_str += dictionary[i]
        if ids_list.index(i) != (len(ids_list) - 1):
            titles_str += "; "
    
    return titles_str


books = pandas.read_csv("../dataset/goodreads_books_clean.csv", low_memory=False)
reviews = pandas.read_csv("../dataset/goodreads_reviews.csv")
books.fillna("Nan", inplace=True)

#dictionary = dict(zip(books.id, books.title))

# books['recommended_books'] = books['recommended_books'].apply(lambda x: replace_id_by_title(dictionary, x))
# books['books_in_series'] = books['books_in_series'].apply(lambda x: replace_id_by_title(dictionary, x))

# reviews["Id"].replace(dictionary, inplace=True)

books['id'] = books['id'].astype('int64')

reviews.rename({'Id': 'book_id', ' Reviews': 'text', ' Users':'user', ' Dates':'date_published'}, axis=1, inplace=True)

# reviews["type"] = "review"
# books["type"] = "book"

reviews['user'].replace({"Vicky phenkos""":'Vicky phenkos'}, inplace=True)

reviews.to_csv('./goodreads_reviews_solr.csv', index = False)
books.to_csv('./goodreads_books_solr.csv', index = False)
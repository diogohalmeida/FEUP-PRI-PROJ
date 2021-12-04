import pandas 

def replace_id_by_title(dictionary, ids_string):
    titles_str = ""
    print(ids_string)
    if pandas.isnull(ids_string):
        return titles_str
    
    ids_list = ids_string.split(',')
    ids_list = list(map(int, ids_list))
    for i in ids_list:
        titles_str += dictionary[i]
        if ids_list.index(i) != (len(ids_list) - 1):
            titles_str += ", "
    
    return titles_str


books = pandas.read_csv("./goodreads_books_clean.csv", low_memory=False)

dictionary = dict(zip(books.id, books.title))

# books['recommended_books'] = books['recommended_books'].apply(lambda x: replace_id_by_title(dictionary, x))

teste = books.loc[books['recommended_books'] == '726458, 726458, 1537534, 3047848, 1651302, 3047851, 561403, 162085, 3047849, 3047850, 162089, 9528186, 6443321, 9893331, 37487, 43207845, 37856897, 52589893, 37486']
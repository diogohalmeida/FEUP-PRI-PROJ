import pandas

dataset = pandas.read_csv("../../dataset/goodreads_books_clean.csv")

#drop columns that have been separated
dataset.drop(columns=['genre_and_votes', 'characters', 'awards'], inplace=True)


dataset.to_csv('../../dataset/goodreads_books_clean.csv', index = False)

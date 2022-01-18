from tempfile import NamedTemporaryFile
import pandas as pd
import json

books_df = pd.read_csv('./dataset/goodreads_books_clean.csv')
reviews_df = pd.read_csv('./dataset/goodreads_reviews.csv')

books = books_df.to_dict(orient='records')

for book in books:
    id = book['id']
    print(id)
    book['reviews'] = reviews_df[reviews_df['Id'] == id][' Reviews'].tolist()

# Save merged data
with open("data.json", "w+") as f:
    f.write(json.dumps(books, indent=4))
    f.close()

print("-> Successfully merged books, genres and reviews\n")
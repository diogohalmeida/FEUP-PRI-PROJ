import pandas

dataset = pandas.read_csv("../../dataset/goodreads_books_clean.csv")
ids = dataset["id"].tolist()
        
characters = []

for id, row in dataset.iterrows():
    if type(row['characters']) != type(float('nan')):
        book_characters = [" ".join(j.split()) for j in row['characters'].split(",")]
        for j in book_characters:
            if j not in characters:
                characters.append((row['id'], j))

characters_frame = pandas.DataFrame(characters,columns=["id","Character"])

characters_frame.to_csv('../../dataset/characters.csv', index = False)

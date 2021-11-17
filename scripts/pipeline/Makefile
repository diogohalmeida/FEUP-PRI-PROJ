SHELL := bash

Default: statistiscs

statistiscs: drop_extracted_columns
	python3 ./development.py

drop_extracted_columns: separate_characters
	python3 ./drop_repeated_columns.py

separate_characters: separate_awards
	python3 ./generate_characters.py

separate_awards: separate_genres_and_votes
	python3 ./generate_awards.py

separate_genres_and_votes: load_and_refine
	python3 ./generate_genres.py

load_and_refine: reviews_scrapper
	python3 ./refine.py
	
reviews_scrapper: requirements
	python3 ../scrape-scripts/reviews.py
	
requirements:        
	pip install -r requirements.txt
#!/bin/bash

precreate-core reviews

precreate-core books

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 10

#mkdir /var/solr/data/books/conf

cp /data/synonyms.txt /var/solr/data/books/conf

mkdir /var/solr/data/books/lib

cp /models/en-ner-person.bin /var/solr/data/books/conf/en-ner-person.bin

cp /models/en-sent.bin /var/solr/data/books/conf/en-sent.bin

cp /models/en-token.bin /var/solr/data/books/conf/en-token.bin

cp contrib/analysis-extras/lib/icu4j-62.1.jar /var/solr/data/books/lib
cp contrib/analysis-extras/lib/opennlp-tools-1.9.2.jar /var/solr/data/books/lib
cp contrib/analysis-extras/lib/morfologik-stemming-2.1.5.jar /var/solr/data/books/lib
#cp contrib/analysis-extras/lib/morfologik-fsa-2.1.5.jar /var/solr/data/books/lib
#cp contrib/analysis-extras/lib/morfologik-polish-2.1.5.jar /var/solr/data/books/lib
#cp contrib/analysis-extras/lib/morfologik-ukrainian-search-4.9.1.jar /var/solr/data/books/lib

cp contrib/analysis-extras/lucene-libs/lucene-analyzers-icu-8.10.1.jar /var/solr/data/books/lib
cp contrib/analysis-extras/lucene-libs/lucene-analyzers-morfologik-8.10.1.jar /var/solr/data/books/lib
cp contrib/analysis-extras/lucene-libs/lucene-analyzers-opennlp-8.10.1.jar /var/solr/data/books/lib
cp contrib/analysis-extras/lucene-libs/lucene-analyzers-smartcn-8.10.1.jar /var/solr/data/books/lib
cp contrib/analysis-extras/lucene-libs/lucene-analyzers-stempel-8.10.1.jar /var/solr/data/books/lib


# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/config.json \
    http://localhost:8983/solr/books/config

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/reviews_schema.json \
    http://localhost:8983/solr/reviews/schema

curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/books/schema
	

# Populate collection
bin/post -c reviews /data/goodreads_reviews_solr.csv

# Populate collection
bin/post -c books /data/goodreads_books_solr.csv

# Restart in foreground mode so we can access the interface
solr restart -f

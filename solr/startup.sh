#!/bin/bash

precreate-core books

# Start Solr in background mode so we can use the API to upload the schema
solr start

sleep 10

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary @/data/schema.json \
    http://localhost:8983/solr/books/schema

# Populate collection
bin/post -c books /data/data.json

# Populate collection
#bin/post -c books /data/goodreads_reviews_solr.csv

# Restart in foreground mode so we can access the interface
solr restart -f

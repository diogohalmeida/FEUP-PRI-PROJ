FROM solr:8.10

COPY goodreads_books_solr.csv /data/goodreads_books_solr.csv

COPY goodreads_reviews_solr.csv /data/goodreads_reviews_solr.csv

COPY schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]

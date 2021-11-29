FROM solr:8.10

COPY goodreads_books_clean.csv /data/goodreads_books_clean.csv

COPY schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]

FROM solr:8.10

ADD models /models

ADD ltr /ltr

COPY config.xml config.xml

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]

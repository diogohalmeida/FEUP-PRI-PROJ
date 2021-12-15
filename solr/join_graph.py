# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd
from itertools import cycle

# setup plot details
colors = cycle(['#95d840ff','#287d8eff','#440154ff'])

QRELS_FILE = "./queries/query2/query2.txt"

QUERY_URL_NORMAL = "http://localhost:8983/solr/books/select?defType=edismax&indent=true&q.op=OR&q=comics%20AND%20(%22spider-man%22%20OR%20spiderman)&qf=title%20genre_and_votes%20description%20characters&rows=10"
QUERY_URL_BOOSTED = "http://localhost:8983/solr/books/select?defType=edismax&indent=true&q.op=OR&q=comics%20AND%20(%22spider-man%22%20OR%20%22Peter%20Parker%22)&qf=title%5E2%20genre_and_votes%5E2%20description%5E1%20characters%5E3&rows=10"

# Read qrels to extract relevant documents
relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance

results_noschema = json.load(open('./queries/query2/noschema.json', encoding="utf8"))['response']['docs']
results_normal = requests.get(QUERY_URL_NORMAL).json()['response']['docs']
results_boosted = requests.get(QUERY_URL_BOOSTED).json()['response']['docs']

results_list = [results_noschema, results_normal, results_boosted]

_, ax = plt.subplots(figsize=(7, 8))

i=0
for results, color in zip(results_list, colors):
    # PRECISION-RECALL CURVE
    # Calculate precision and recall values as we move down the ranked list
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
            if doc['id'] in relevant
        ]) / idx 
        for idx, _ in enumerate(results, start=1)
    ]

    recall_values = [
        len([
            doc for doc in results[:idx]
            if doc['id'] in relevant
        ]) / len(relevant)
        for idx, _ in enumerate(results, start=1)
    ]

    precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

    # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
    recall_values.extend([step for step in np.arange(0, 1.1, 0.1) if step not in recall_values])
    recall_values = sorted(set(recall_values))

    # Extend matching dict to include these new intermediate steps
    for idx, step in enumerate(recall_values):
        if step not in precision_recall_match:
            if recall_values[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

    disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
    if(i==0):
        disp.plot(ax=ax, name=f"Precision-recall without schema", color=color, linewidth=3)
    elif(i==1):
        disp.plot(ax=ax, name=f"Precision-recall without boost", color=color, linewidth=1.5)
    elif(i==2):
        disp.plot(ax=ax, name=f"Precision-recall with boost", color=color, linewidth=1)
    i+=1

# add the legend for the iso-f1 curves
handles, labels = disp.ax_.get_legend_handles_labels()

# set the legend and the axes
ax.legend(handles=handles, labels=labels, loc="best")
ax.set_title("Precision-Recall curve to Query 4")

plt.savefig('precision_recall.pdf')

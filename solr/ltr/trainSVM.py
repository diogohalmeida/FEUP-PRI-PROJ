import itertools
import numpy as np
import sklearn as sk
import pandas as pd
import requests
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, plot_confusion_matrix
from sklearn import svm, linear_model
from pairwiseSVM import RankSVM
from sklearn.model_selection import KFold
import pairwiseSVM


import simplejson

qrels_prefix = "../queries/query"
qrels_sufix = ".txt"

queries_urls = [
    "http://localhost:8983/solr/books/select?defType=edismax&fl=*%2Cid%2Cscore%2C%5Bfeatures%5D&indent=true&q.op=OR&q=hitler%20AND%20biography&qf=title%5E3%20genre_and_votes%5E2%20description%5E1%20author%5E3&rows=92&rq=%7B!ltr%20model%3Dmy_efi_model%20efi.text%3D%22hitler%20biography%22%7D",
    "http://localhost:8983/solr/books/select?defType=edismax&fl=*%2Cid%2Cscore%2C%5Bfeatures%5D&indent=true&q.op=OR&q=comics%20AND%20(%22spider-man%22%20OR%20%22Peter%20Parker%22)&qf=title%5E3%20genre_and_votes%5E2%20description%5E1%20characters%5E2%20ner_person_field%5E2&rows=31&rq=%7B!ltr%20model%3Dmy_efi_model%20efi.text%3D%22spider-man%22%7D",
    "http://localhost:8983/solr/books/select?defType=edismax&fl=*%2Cid%2Cscore%2C%5Bfeatures%5D&indent=true&q.op=OR&q=einstein%20AND%20-fiction%20AND%20(philosophy%20OR%20science)&qf=title%5E3%20genre_and_votes%5E2%20description%5E1%20characters%5E3%20ner_person_field%5E3&rows=100&rq=%7B!ltr%20model%3Dmy_efi_model%20efi.text%3D%22einstein%20science%22%7D",
    "http://localhost:8983/solr/books/select?defType=edismax&fl=*%2Cid%2Cscore%2C%5Bfeatures%5D&fq=description%3Akingdom&fq=genre_and_votes%3Achildrens&fq=genre_and_votes%3Afantasy&indent=true&pf=reviews%5E5&ps=5&q.op=OR&q=%22easy%20read%22&qf=reviews%5E2&rows=100&rq=%7B!ltr%20model%3Dmy_efi_model%20efi.text%3D%22kingdom%22%7D"
    ]

total_features = []
def extract_features(url, qid):
    response = requests.request("GET", url)
    json = simplejson.loads(response.text)
    
    file = qrels_prefix + str(qid) + "/" + "query" + str(qid) + qrels_sufix
    relevant_docs = [x.split(" ")[0] for x in open(file).readlines()]
    
    documents = json["response"]["docs"]
    for idx, doc in enumerate(documents):
        features = doc["[features]"].split(",")
        features_numerical = list(map(lambda x: float(x.split("=")[1]), features))
        if doc["id"] in relevant_docs:
            features_numerical.append(1)
        else: features_numerical.append(-1)
        features_numerical.append(qid)
        total_features.append(features_numerical)

        
for idx, url in enumerate(queries_urls):
    extract_features(url, idx+1)

df = pd.DataFrame(total_features, columns=["maximize_rating", "maximize_average_rating", "maximize_recommendation_number", "description_bm25", "original_score", "status", "qid"])

df_X = df.drop(columns = ["status", "qid"])
df_y = df[["status", "qid"]]

X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size = 0.20)


"""
    POINTWISE APPROACH
"""
# param_grid = {'C': [0.1, 1, 10, 100, 1000],
#               'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
#               'kernel': ["linear"]}

# grid = GridSearchCV(SVC(), param_grid, scoring="recall")

# grid.fit(X_train, y_train)

# prediction = grid.predict(X_test)

# print(classification_report(y_test, prediction))
# plot_confusion_matrix(grid.best_estimator_, X_test, y_test)  

"""
    PAIRWISE APPROACH
"""

rank_svm = RankSVM().fit(X_train.to_numpy(), y_train.to_numpy())
print('Performance of SVM ranking ', rank_svm.score(X_test.to_numpy(),y_test.to_numpy()))


# # and that of linear regression
# ridge = linear_model.RidgeCV(fit_intercept=True)
# ridge.fit(X_train.to_numpy(), y_train.to_numpy())
# X_test_trans, y_test_trans = pairwiseSVM.transform_pairwise(X_test.to_numpy(), y_test.to_numpy())
# score = np.mean(np.sign(np.dot(X_test_trans, ridge.coef_)) == y_test_trans)
# print('Performance of linear regression ', score)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from fuzzywuzzy import fuzz


def fakenewsdetection(data):
    confirmed = 0
    confirm_score = 0
    df = pd.read_csv('data/coviddata.csv')
    truefalse = df.outcome
    x_train, x_test, y_train, y_test = train_test_split(df['title'], truefalse, test_size=0.1)
    tfidf = TfidfVectorizer(stop_words='english', max_df=0.9)
    tfidf_train = tfidf.fit_transform(x_train)
    tfidf_test = tfidf.transform(x_test)
    model = linear_model.LogisticRegression(max_iter=1000)
    model.fit(tfidf_train, y_train)
    y_pred = model.predict(tfidf_test)
    acc = accuracy_score(y_test, y_pred)
    print(acc)
    vect = tfidf.transform(data).toarray()
    proba = model.predict_proba(vect)
    for i in df['title']:
        if fuzz.ratio(i, data[0]) > 90:
            confirmed = 1
            confirm_score = fuzz.ratio(i, data[0])

    return [model.predict(vect)[0], proba[0][0]*100, proba[0][1]*100, confirmed, confirm_score]
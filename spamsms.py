import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def spamsmsdetection(data):
    df = pd.read_csv("data/spam.csv", encoding="latin-1")
    x = df['v2']
    y = df['v1']
    le = LabelEncoder()
    y = le.fit_transform(y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=7, test_size=0.2)
    c = CountVectorizer(ngram_range=(1,2))
    x_train = c.fit_transform(x_train)
    l = LogisticRegression(max_iter = 10000)
    l.fit(x_train, y_train)

    prediction = l.predict(c.transform(x_test))
    a = accuracy_score(y_test, prediction)

    return l.predict(c.transform(data))[0]



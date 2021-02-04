import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
from sklearn import naive_bayes
import sklearn
from sklearn.metrics import accuracy_score, confusion_matrix


def fakenewsdetection(data):
    exist = 0
    df = pd.read_csv('data/coviddata.csv')
    df1 = pd.DataFrame(df)
    # df2 = df1[(df1['confirm'] == 1) & (df1['true_false'] == 0)]

    truefalse = df.outcome
    x_train, x_test, y_train, y_test = train_test_split(df['title'], truefalse, test_size=0.1, shuffle=True, random_state=100)
    tfidf = TfidfVectorizer(stop_words='english', max_df=1.0)
    tfidf_train = tfidf.fit_transform(x_train)
    tfidf_test = tfidf.transform(x_test)
    model = linear_model.PassiveAggressiveClassifier(max_iter=10000)
    model.fit(tfidf_train, y_train)
    y_pred = model.predict(tfidf_test)
    acc = accuracy_score(y_test, y_pred)
    print(acc)
    vect = tfidf.transform(data).toarray()
    return model.predict(vect)[0]
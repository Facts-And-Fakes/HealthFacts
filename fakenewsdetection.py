import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


def fakenewsdetection(data):
    exist = 0
    df = pd.read_csv('data/NewsData.csv')
    df1 = pd.DataFrame(df)
    df2 = df1[(df1['confirm'] == 1) & (df1['true_false'] == 0)]
    df2 = df2[['title', 'date', 'avgReview']]

    truefalse = df.true_false

    x_train, x_test, y_train, y_test = train_test_split(df['news'], truefalse, test_size=0.3, shuffle=True, random_state=42)

    tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)

    tfidf_train = tfidf.fit_transform(x_train)
    tfidf_test = tfidf.transform(x_test)

    PAClass = PassiveAggressiveClassifier(max_iter=10)
    PAClass.fit(tfidf_train, y_train)

    y_pred = PAClass.predict(tfidf_test)
    acc = accuracy_score(y_test, y_pred)

    confusion_matrix(y_test, y_pred, labels=[0, 1])
    resultsConf = 0
    vect = tfidf.transform(data).toarray()
    return PAClass.predict(vect)[0]
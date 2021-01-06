from flask import Flask,render_template,url_for,request, Response, redirect
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

app = Flask(__name__)
newNews = {}
@app.route('/')
def index():
    return render_template("home.html")


@app.route('/fakenews')
def home():
    df = pd.read_csv('data/NewsData.csv')
    sources = pd.read_csv('data/newssources.csv')
    df1 = pd.DataFrame(df)
    df2 =  df1[(df1['confirm'] == 1) & (df1['true_false'] == 0)]
    df2 = df2[['title', 'date','avgReview']]
    return render_template('index.html', tables=[df2.to_html(classes='data', header="true")],  titles = df2.columns.values, tables1=[sources.to_html(classes='data', header="true")],  titles1 = sources.columns.values)

@app.route('/predict',methods=['POST'])
def predictFake():
    exist = 0
    df = pd.read_csv('data/NewsData.csv')
    df1 = pd.DataFrame(df)
    df2 =  df1[(df1['confirm'] == 1) & (df1['true_false'] == 0)]
    df2 = df2[['title', 'date','avgReview']]
    
    truefalse = df.true_false

    x_train,x_test,y_train,y_test = train_test_split(df['news'], truefalse, test_size = 0.3, shuffle = True, random_state = 42)

    tfidf = TfidfVectorizer(stop_words = 'english', max_df = 0.7)

    tfidf_train = tfidf.fit_transform(x_train) 
    tfidf_test = tfidf.transform(x_test)

    PAClass = PassiveAggressiveClassifier(max_iter = 10)
    PAClass.fit(tfidf_train,y_train)

    y_pred = PAClass.predict(tfidf_test)
    acc = accuracy_score(y_test,y_pred)
    print('Model Accuracy: {}'.format(round(acc*100,1)))
    
    confusion_matrix(y_test,y_pred, labels=[0,1])
    resultsConf = 0
    if request.method == 'POST':
        message = request.form['message']
        exist = message in df1.title or message in df1.news
        source = request.form['source']
        date = request.form['date']
        news = '{} - {}'.format(source, message)
        data = [message]
        vect = tfidf.transform(data).toarray()
        model_prediction = PAClass.predict(vect)
        if exist == 1:
            newNews = df1[df1['title'] == message or df1['news'] == message]
            resultsConf = 1
        if exist == 0:
            newNews = pd.DataFrame({
                'title' : message,
                'news' : news,
                'date' : date,
                'true_false' : model_prediction,
                'confirm' : False,
                'numReviews' : 0,
            })
            resultsConf = 0
        df1.append(newNews, ignore_index = True)
        df1.to_csv('NewsData.csv')
    return render_template('result.html',resultsConf = resultsConf, prediction = model_prediction, tables=[df2.to_html(classes='data', header="true")],  titles = df2.columns.values, newNews = newNews, message = message)


@app.route("/fakereviews")
def fakereviews():
    return render_template("fakereviews.html")


@app.route("/fakereviewresults")
def fakereviewresults():
    df = pd.read_csv("data/deceptive-opinion.csv")
    source = df['source']
    deceptive = df['deceptive']
    x = df['source'] + ' - ' + df['hotel'] + ' - ' + df['text']
    print(x)
    y = df['deceptive']
    le = LabelEncoder()
    y = le.fit_transform(y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=7, test_size=0.3)
    CountV = CountVectorizer(ngram_range=(1, 2))
    x_train = CountV.fit_transform(x_train)
    l = LogisticRegression(max_iter=10000)
    l.fit(x_train, y_train)

    prediction = l.predict(CountV.transform(x_test))
    a = accuracy_score(y_test, prediction)
    model_prediction = [0]
    print("Model accuracy: {}".format(a * 100))
    if request.method == 'POST':
        message = request.form['message']
        exist = message in df.title or message in df.news
        source = request.form['source']
        date = request.form['date']
        news = '{} - {}'.format(source, message)
        data = [message]
        model_prediction = l.predict(CountV.transform(data))
    return render_template("fakereviewresults.html", predictiondd=model_prediction)

if __name__ == '__main__':
    app.run()

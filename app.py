from flask import Flask,render_template,url_for,request, Response, redirect, session, g, abort
import pandas as pd
from fakeReviewsDetector import fakereviewsdetection
from fakenewsdetection import fakenewsdetection
from spamsms import spamsmsdetection
from passlib.hash import sha256_crypt
import json

global user


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

user = User(id=0, username="Guest", password="")
admin = User(id=1, username="admin", password="admin")
admin2 = User(id=2, username="admin2", password="admin2")

app = Flask(__name__)
secure = open("database.json", "r+")

users = json.load(secure)

update = {admin.username:{"id": admin.id, "password": sha256_crypt.hash(admin.password)}, admin2.username:{"id": admin2.id, "password": sha256_crypt.hash(admin2.password)}}

users.update(update)

with open("database.json", "w") as writefile:
    json.dump(users, writefile)

print(users)
app.secret_key = 'veryverysecret'

newNews = {}

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/profile')
def profile():
    return render_template('profile.html', name=user.username)

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
    df2 = df1[(df1['confirm'] == 1) & (df1['true_false'] == 0)]
    df2 = df2[['title', 'date', 'avgReview']]
    if request.method == 'POST':
        message = request.form['message']
        exist = message in df1.title or message in df1.news
        source = request.form['source']
        news = '{} - {}'.format(source, message)
        data = [message]
        model_prediction = fakenewsdetection(data)
        resultsConf = 0
    return render_template('result.html',resultsConf=resultsConf, prediction=model_prediction, tables=[df2.to_html(classes='data', header="true")],  titles = df2.columns.values, newNews = newNews, message = message)


@app.route("/fakereviews")
def fakereviews():
    return render_template("fakereviews.html")


@app.route("/fakereviewresults", methods=['GET', 'POST'])
def fakereviewresults():
    model_prediction = [0]
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        model_prediction = fakereviewsdetection(data)
    return render_template("fakereviewresults.html", prediction=model_prediction)

@app.route("/login", methods=["GET", "POST"])
def login():
    global user
    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form.get('username')
        passw = request.form.get("password")
        filtered_dict = {k:v for (k,v) in users.items() if username == k}
        print(filtered_dict)
        key = list(filtered_dict.keys())[0]
        userdict = dict(users.get(key))
        print(userdict)
        user = User(id=userdict.get("id"), username=key, password=userdict.get("password"))
        print("\n")
        print(passw)
        print(user.password)
        print("\n")
        verified = sha256_crypt.verify(passw, user.password)
        print(verified)
        if verified:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/signup", methods=['GET', "POST"])
def signup():
    return render_template("signup.html")


@app.route("/signup-done", methods=["POST"])
def signup_done():
    username = request.form['username']
    password = request.form['password']

    last_key = list(users.keys())[-1]
    last_id_dict = dict(users.get(last_key))
    last_id = last_id_dict.get("id")
    print(last_id)

    filtered_dict = {k: v for (k, v) in users.items() if username == k}



    if filtered_dict != {}:  # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('signup'))


    new_user = User(id=last_id+1, username=username, password=sha256_crypt.hash(password))
    print(sha256_crypt.hash(new_user.password))
    print(sha256_crypt.verify("ollol", new_user.password))
    # add the new user to the database
    update = {new_user.username:{"id": new_user.id, "password": new_user.password}}
    users.update(update)
    print(update)
    with open("database.json", "w") as writefile:
        json.dump(users, writefile)
    print(users)

    return redirect(url_for('login'))


@app.route("/spamdetection")
def spam():
    return render_template("spamemailsms.html")

@app.route("/spamresults", methods=["GET","POST"])
def spamresults():
    model_prediction = [0]
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        model_prediction = spamsmsdetection(data)
    return render_template("spamemailsmsresults.html", prediction=model_prediction)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('not-found-page.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

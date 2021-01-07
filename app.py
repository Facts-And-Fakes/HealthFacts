from flask import Flask,render_template,url_for,request, Response, redirect, session, g, abort
import pandas as pd
from fakeReviewsDetector import fakereviewsdetection
from fakenewsdetection import fakenewsdetection
from spamsms import spamsmsdetection
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt

password1 = sha256_crypt.hash("password")
password2 = sha256_crypt.hash("password")

print(password1)
print(password2)

print(sha256_crypt.verify("password", password1))

import json

db = SQLAlchemy()

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User: {}, Password: {}>".format(self.username, sha256_crypt.hash(self.password))

admin = User(id=1, username="admin", password="admin")

app = Flask(__name__)
secure = open("database.json", "r+")

users = json.load(secure)

update = {admin.id:{"username": admin.username, "password": sha256_crypt.hash(admin.password) }}

users.update(update)

with open("database.json", "w") as writefile:
    json.dump(users, writefile)

print(users)
app.secret_key = 'veryverysecret'

newNews = {}

@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('profile.html')

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
        date = request.form['date']
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
    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]

        if sha256_crypt.verify(password, user.password):
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/signup", methods=['GET', "POST"])
def signup():
    return render_template("signup.html")


@app.route("/signup-done", methods=["POST"])
def signup_done():
    username = request.form['username']
    password = request.form['password']

    user = [x for x in users if x.username == username]

    if user != []:  # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('login'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(id="s", username=username, password=sha256_crypt.hash(password))

    # add the new user to the database
    update = {new_user.id:{"username": new_user.username, "password": sha256_crypt.hash(new_user.password)}}
    users.update(update)
    with open("database.json", "w") as writefile:
        json.dump(users, writefile)

    print(users)

    return redirect(url_for('auth.login'))


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
    # note that we set the 404 status explicitly
    return render_template('not-found-page.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

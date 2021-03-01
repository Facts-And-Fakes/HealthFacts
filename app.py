# Importing libraries
from flask import Flask, render_template, url_for, request, redirect, session
import pandas as pd
from fakenewsdetection import fakenewsdetection
from questions import query
from passlib.hash import sha256_crypt
import json
from googleSearch import googleSearch

# Defining some global variables
failed = False
signup_failed = False


# Defining a user class containing ID, username and password


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


admin = User(id=1, username="admin", password="admin")
admin2 = User(id=2, username="admin2", password="admin2")
app = Flask(__name__)
secure = open("database.json", "r+")
users = json.load(secure)

with open("database.json", "w") as writefile:
    json.dump(users, writefile)

app.secret_key = 'veryverysecret'
newNews = {}

# main page


@app.route('/')
def index():
    session['feature'] = 'none'
    return render_template("home.html")


# profile page

@app.route('/profile')
def profile():
    user = User(id=session['user_id'], username=session['username'], password="")
    if session.get("logged_in") is True and not session.get('user_id') is None:
        return render_template('profile.html', name=user.username)
    else:
        return render_template("not-logged-in.html")


# prediction pages


@app.route('/fakenews')
def home():
    df = pd.read_csv('data/NewsData.csv')
    sources = pd.read_csv('data/newssources.csv')
    df1 = pd.DataFrame(df)
    df2 = df1[(df1['confirm'] == 1) & (df1['true_false'] == 0)]
    df2 = df2[['title', 'date','avgReview']]
    return render_template('index.html', tables=[df2.to_html(classes='data', header="true")],  titles = df2.columns.values, tables1=[sources.to_html(classes='data', header="true")],  titles1 = sources.columns.values)


@app.route('/predict',methods=['POST'])
def predictFake():
    resultsconf = 0
    model_prediction = 0
    message = ["No news given"]
    df = pd.read_csv('data/NewsData.csv')
    df1 = pd.DataFrame(df)
    df2 = df1[(df1['confirm'] == 1) & (df1['true_false'] == 0)]
    df2 = df2[['title', 'date', 'avgReview']]
    if request.method == 'POST':
        message = request.form['message']
        session['news'] = message
        session['feature'] = 'fakenewsdetection'
        exist = message in df1.title or message in df1.news
        source = request.form['source']
        news = '{} - {}'.format(source, message)
        data = [message]
        model_prediction = fakenewsdetection(data)
        resultsconf = 0
    return render_template('result.html', prediction=model_prediction[0], proba1=model_prediction[1], proba2=model_prediction[2], c=model_prediction[3], cs=model_prediction[4], tables=[df2.to_html(classes='data', header="true")],  titles=df2.columns.values, newNews=newNews, message=message)


@app.route('/report', methods=['GET', 'POST'])
def report():
    if not session['logged_in']:
        return render_template('login.html', failed=False, plslogin=True)
    return render_template('report.html', news=session['news'])


@app.route('/report-placed', methods=['GET', 'POST'])
def reported():
    if request.method == 'POST':
        df = pd.read_csv('data/reports.csv')
        report_msg = str(request.form.get('news'))
        comment = str(request.form.get('comment'))
        reporter = session['username']
        feature = session['feature']
        df.loc[len(df.index)] = [report_msg, comment, reporter, feature]
        df.to_csv('data/reports.csv', index=False)

    return render_template('report-placed.html')


@app.route("/questions", methods=["GET", "POST"])
def questions():
    return render_template("questions.html")


@app.route("/query-results", methods=['GET', 'POST'])
def query_results():
    if request.method == "POST":
        ques = request.form.get("query")
        session['news'] = ques
        session['feature'] = 'questions'
        x = query(ques)
        y = googleSearch(ques)
        if ques == '':
            return render_template("questions.html", error="Input cannot be empty")
        if x == 'error none found':
            return render_template("query-results.html", q=ques, o='', a='Sorry, no results were found.', useful_results=y)
        return render_template("query-results.html", q=x[0], o=x[1], a=x[2], useful_results=y)



# login, logout, signup


@app.route("/login", methods=["GET", "POST"])
def login():
    global user
    if request.method == "POST":
        try:
            session.pop("user_id", None)
            username = request.form.get('username')
            passw = request.form.get("password")
            filtered_dict = {k:v for (k,v) in users.items() if username == k}
            key = list(filtered_dict.keys())[0]
            userdict = dict(users.get(key))
            user = User(id=userdict.get("id"), username=key, password=userdict.get("password"))
            verified = sha256_crypt.verify(passw, user.password)
            if verified:
                failed = False
                session['user_id'] = user.id
                session['logged_in'] = True
                session['username'] = user.username
                return redirect(url_for('profile'))
            else:
                failed=True
                return render_template("login.html", failed=True, plslogin=False)
        except:
            failed = True
            return render_template("error.html")

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
    filtered_dict = {k: v for (k, v) in users.items() if username == k}
    if filtered_dict != {}:  # if a user is found, we want to redirect back to signup page so user can try again
        signup_failed = True
        return render_template('signup.html', signup_failed=True)
    new_user = User(id=last_id+1, username=username, password=sha256_crypt.hash(password))
    # add the new user to the database
    update = {new_user.username:{"id": new_user.id, "password": new_user.password}}
    users.update(update)
    with open("database.json", "w") as writefile:
        json.dump(users, writefile)
    signup_failed = False

    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template("logged-out.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not-found-page.html'), 404


if __name__ == '__main__':
    app.run()

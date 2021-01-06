import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

df = pd.read_csv("data/deceptive-opinion.csv")
source = df['source']
deceptive = df['deceptive']
x = df['source']+' - '+df['hotel']+' - '+df['text']
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
print("Model accuracy: {}".format(a*100))
plt.plot(source, deceptive)
plt.show()
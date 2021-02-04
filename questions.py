import pandas as pd
from fuzzywuzzy import fuzz

df = pd.read_csv("data/covidquestions.csv", encoding="latin-1")
titles = df['title']+df['news_url']
print(df.iloc[df["title"]=="What areas should be prioritized for disinfection in non-health care settings?", "news_url"])
print(titles.head())

def query(q):
    df = pd.read_csv("data/covidquestions.csv")
    titles = df['title']
    results = []
    links = []
    for title in titles:
        if fuzz.ratio(title, q) > 80:
            results.append(title)
    return df.query("title=={}".format(title))['news_url']

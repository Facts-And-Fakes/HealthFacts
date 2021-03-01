import pandas as pd
from fuzzywuzzy import fuzz


def query(q):
    try:
        df = pd.read_csv("data/COVID-Q-master/final_master_dataset.csv", encoding="latin-1")
        titles1 = df['Question']
        result = ''
        others = []
        prev_ratio = 40
        for title in list(titles1):
            if isinstance(title, float):
                continue
            ratio = fuzz.ratio(title, q)
            if ratio > prev_ratio:
                prev_ratio = ratio
                others.append([title, ratio])
                result = title
        x = []
        otherresult = []
        for other in others:
            x.append(other[1])
        y = x
        y.sort(reverse=True)
        for i in range(len(x)):
            if i == 4:
                break
            otherresult.append(others[x.index(y[i])])

        return [result, otherresult, str(list(df[df['Question'] == result]['Answers'])[0])]
    except:
        return ["No results found", ["No results found"], "No results found"]

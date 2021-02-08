import pandas as pd

df = pd.read_csv('data/reports.csv')
reporter = 'report'
comment = 'report'
df.loc[len(df.index)] = [reporter, comment]
df.to_csv('data/reports.csv', index=False)

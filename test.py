import pandas as pd
x = pd.read_csv('pnr.csv',dtype='object')
x.drop(1,axis=0,inplace=True)
print(x)
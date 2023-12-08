import pandas as pd
x = pd.read_html('https://www.totaltraininfo.com/train/12309/schedule')
print(x[1])
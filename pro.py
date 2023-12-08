import pandas as pd
x = pd.read_html('https://etrain.info/train/12001/schedule')
import re
y = x[5]
print(y)
'''x = pd.read_html('https://erail.in/train-enquiry/12910')
print(x)'''
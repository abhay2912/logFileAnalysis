import mpld3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Data for plotting
# df = pd.read_csv("prediction/NumPredictedCSV.csv")
# t = df['0','1','2','3','4','5','6']
# s = df['7']
# plt.scatter(df["1"], df["3"])

from pylab import randn
t = randn(200)
s = randn(200)

# t = [0.1,14,2]
# s = [1,2,2]
fig, ax = plt.subplots()
ax.plot(t, s)
plt.xlabel("X")
plt.ylabel("Y")

ax.grid()

html_str = mpld3.fig_to_html(fig, figid = 'fig2', no_extras=False)
html_doc = f'''
<link rel="stylesheet" type="text/css" href="static/css/fig.css">
<script src="../static/js/script.js"></script>
{html_str}
'''
Html_file= open("templates/fig.html","w")
Html_file.write(html_doc)
Html_file.close()
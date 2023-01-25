import mpld3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Data for plotting
df = pd.read_csv("prediction/NumPredictedCSV.csv")
t = df['0','1','2','3','4','5','6']
s = df['7']
plt.scatter(df["1"], df["3"])

# fig, ax = plt.subplots()
# ax.plot(t, s)

# ax.set(xlabel='time (s)', ylabel='voltage (mV)',
#        title='About as simple as it gets, folks')
# ax.grid()
# fig2, ax = plt.subplots()
# ax.plot(s, t)
# ax.set(xlabel='sdfgdg (s)', ylabel='voadfasdltage (mV)',
#        title='About as simple as it gets, folks')
# ax.grid()
# fig.savefig("test.png")
# plt.show()

# html_str = mpld3.fig_to_html(fig)
# Html_file= open("index2.html","w")
# Html_file.write(html_str)


html_str = mpld3.fig_to_html(fig, figid = 'fig2', no_extras=False)

html_doc = f'''
<link rel="stylesheet" type="text/css" href="static/css/fig.css">
<script src="../static/js/script.js"></script>

{html_str}
'''
# <style type="text/css">
# div#fig1 {{ text-align: center }}
# </style>
Html_file= open("templates/fig.html","w")
Html_file.write(html_doc)
Html_file.close()

# print(html_doc)
# html_str = mpld3.fig_to_html(fig2)
# # Html_file= open("index2.html","w")
# Html_file.write(html_str)

# Html_file.close()
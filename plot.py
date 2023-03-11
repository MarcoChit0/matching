from math import log
import os
import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

datapath = '/home/macsilva/Desktop/ufrgs/cadeiras/2022/02/alg_avancados/matching/execs'
tablespath = '/home/macsilva/Desktop/ufrgs/cadeiras/2022/02/alg_avancados/matching/tables/'
rgraphspath = '/home/macsilva/Desktop/ufrgs/cadeiras/2022/02/alg_avancados/matching/rgraphs_execs'
dfs = pd.DataFrame()
graph_sizes = []

for file in os.listdir(datapath):
    strn, sort = file.split('_')
    n = int(strn.replace('ap', ''))
    df = pd.read_csv(datapath + '/' + file)
    df['file'] = file
    df['sort'] = int(sort.replace('.csv', ''))
    df['gsize'] = n
    if n not in graph_sizes:
        graph_sizes.append(n)
    dfs = dfs.append(df)

for n in graph_sizes:
    df = dfs.loc[dfs['gsize']==n].groupby(['file']).mean().reset_index().sort_values(by='sort')
    with open(tablespath + str(n) + '.tex', 'w') as tf:
        tf.write(df[['file', 'time']].to_latex(index_names=False))

df = dfs.groupby(['gsize']).mean().reset_index()
plt.clf()
sns.barplot(x='gsize', y='time', data=df)
plt.xlabel('graph size')
plt.ylabel('time')
plt.savefig('/home/macsilva/Desktop/ufrgs/cadeiras/2022/02/alg_avancados/matching/plots/sizecomp.png')

rgraphs_dfs = pd.DataFrame()
for file in os.listdir(rgraphspath):
    rdf = pd.read_csv(rgraphspath + '/' + file)
    rdf['gsize'] = int(file.split('.')[0])
    rdf['time'] = rdf['time']
    rgraphs_dfs = rgraphs_dfs.append(rdf)

print(rgraphs_dfs)
rgraphs_dfs = rgraphs_dfs.sort_values(by='gsize')
print(rgraphs_dfs)
plt.clf()
sns.lmplot(
    data=rgraphs_dfs, 
    x='gsize',
    y='time',
    order=2, 
    ci=None, 
    scatter_kws={"s": 10}, 
    line_kws={'lw':2, "color": "red"}
    )
plt.xlabel('graph size')
plt.ylabel('time')
plt.savefig('/home/macsilva/Desktop/ufrgs/cadeiras/2022/02/alg_avancados/matching/rgraphs_plots/sizextime.png')

plt.clf()

lp_df = rgraphs_dfs.groupby(['gsize']).mean().sort_values(by='gsize').reset_index()
lp_df['comp'] = lp_df['time'] / (lp_df['gsize'] * \
(((lp_df['gsize'] * lp_df['gsize']) + lp_df['gsize'])\
* np.log2(lp_df['gsize'])))

sns.lmplot(
    x='gsize',
    y='comp',
    data= lp_df,
    order=7, 
    ci=None, 
    scatter_kws={"s": 10, "color": "green"}, 
    line_kws={'lw':2, "color": "purple"}
)
plt.xlabel('graph size')
plt.ylabel('time')
plt.savefig('/home/macsilva/Desktop/ufrgs/cadeiras/2022/02/alg_avancados/matching/rgraphs_plots/comparisiontimebyexpected.png')

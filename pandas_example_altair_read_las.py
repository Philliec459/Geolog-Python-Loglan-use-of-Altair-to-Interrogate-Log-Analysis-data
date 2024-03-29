#!/usr/bin/env python3
# python loglan

# Imports
#########import geolog

from pandas import DataFrame, read_csv

import altair as alt
alt.renderers.enable('altair_viewer')

import pandas as pd
import numpy as np
import altair_transform
import lasio



# Load data from geolog
##########while geolog.gettable():
##########indent all lines below if using Geolog Python Loglan





'''
  select the proper Neutron-Denisity Chartbook file
'''
#file = r'./data/cnl_chart_1pt0.xlsx'
file = r'./data/cnl_chart_1pt1.xlsx'
#file = r'./data/tnph_chart_1pt0.xlsx'
#file = r'./data/tnph_chart_1pt19.xlsx'
df_chart = pd.read_excel(file,index_col=False)
df_chart.head()





'''
  PEF vs. RHOB overlay
'''  
#Load PEF vs. RHOB overlay chart
file = r'./data/PEF_Rhob_chart.xlsx'
df_pef = pd.read_excel(file,index_col=False)
df_pef.head()



'''
  Pickett Plot
'''  
#select the proper Pickett data
#Adjust the Rw and m in the file designated below.

file = r'./data/Pickett_Ro_chart.xlsx'

df_pickett = pd.read_excel(file,index_col=False)
df_pickett.head()



'''
  read in las file using lasio
'''  
las = lasio.read("./data/GulfCoast_NMR2.las")
df = las.df()
df = df.rename_axis('DEPTH').reset_index()
df.head(20)
 


interval = alt.selection_interval()




'''
   Define Zone of Interest for the depth plots. Xplots??? Histograms??? 
'''
#top    = 4000
#bottom = 5000

top    = 4500
bottom = 4750



'''
 Altair Interactive Plotting
'''
base=alt.Chart(df).mark_point(clip=True).encode(
    alt.Y('DEPTH:Q',
        scale=alt.Scale(domain=(bottom, top))
    ),
).properties(
    width=100,
    height=500,
    #title='GR',
    selection=interval
)



base2=alt.Chart(df).mark_point(clip=True).encode(
    alt.Y('DEPTH:Q',
        scale=alt.Scale(domain=(bottom, top)), axis=alt.Axis(labels=False),title='',
    ),
).properties(
    width=100,
    height=500,
    title='',
    selection=interval
)




gr = base.mark_circle(clip=True, size=30).encode(
    x='GR:Q',  
    #size=('PHIX:Q'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(domain=(0, 150),scheme='rainbow'),legend=None),
    #color=alt.condition(selector, 'Well_Name:O', alt.value('lightgray'), legend=None),
    tooltip='GR:Q', 
).properties(
    title='GR',
    selection=interval
)


rhob = base2.mark_circle(clip=True , size=10).encode(
    alt.X('RHOB:Q',
        scale=alt.Scale(domain=(1.65, 2.65))
    ),     
    #color=alt.value('red'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    #color=alt.condition(selector, 'Well_Name:O', alt.value('lightgray'), legend=None),
    tooltip='RHOB:Q', 
).properties(
    title='RHOB',
    selection=interval
)


nphi = base2.mark_circle(clip=True, size=10).encode(
    alt.X('NPHI:Q',
        scale=alt.Scale(domain=(.6, 0))
    ),     
    #y=('DEPTH'),
    #color=alt.value('green'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='NPHI:Q', 
).properties(
    title='NPHI',
    selection=interval
)


rt = base2.mark_circle(clip=True, size=10).encode(
    alt.X('ILD:Q', 
          scale=alt.Scale(type='log')
    ),
    #x='LRT:Q',  
    #y=('DEPTH'),
    #color=alt.value('black'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='ILD:Q', 
).properties(
    title='ILD',
    selection=interval
)




phit = base2.mark_circle(clip=True, size=10).encode(
    alt.X('PHIX:Q',
        scale=alt.Scale(domain=(.6, 0))
    ),    
    #color=alt.value('blue'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='PHIX:Q', 
).properties(
    title='PHIX',
    selection=interval
)

mbvi = base2.mark_circle(clip=True, size=10).encode(
    alt.X('MBVI:Q',
        scale=alt.Scale(domain=(.6, 0))
    ),    
    #color=alt.value('blue'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='MBVI:Q', 
).properties(
    title='MBVI',
    selection=interval
)

mphi = base2.mark_circle(clip=True, size=10).encode(
    alt.X('MPHI:Q',
        scale=alt.Scale(domain=(.6, 0))
    ),    
    #color=alt.value('red'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='MPHI:Q', 
).properties(
    title='MPHI',
    selection=interval
)





nd_chart = alt.Chart(df_chart).mark_line().encode(
    alt.X('CNL_chart:Q',
        scale=alt.Scale(domain=(-0.05, 0.6))
    ),    
    alt.Y('RHOB_chart:Q',
        scale=alt.Scale(domain=(3, 1.9))
    ),    
    color=alt.condition(interval, 'Lith:O', alt.value('black'),scale=alt.Scale(scheme='sinebow'),legend=None),
    #color=alt.value('black'),
).properties(
    #title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250
    #selection=interval
)

nd_chart2 = alt.Chart(df_chart).mark_line().encode(
    alt.X('CNL_chart:Q',
        scale=alt.Scale(domain=(-0.05, 0.6))
    ),    
    alt.Y('RHOB_chart:Q',
        scale=alt.Scale(domain=(3, 1.9))
    ),    
    color=alt.condition(interval, 'Por:O', alt.value('black'),scale=alt.Scale(scheme='rainbow'),legend=None),
    #color=alt.value('black'),
).properties(
    #title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250
    #selection=interval
)

ndxplot = base.mark_circle(size=20).encode(
    alt.X('NPHI:Q',
        scale=alt.Scale(domain=(-0.05, 0.6))
    ),    
    alt.Y('RHOB:Q',
        scale=alt.Scale(domain=(3, 1.9))
    ),    
    #x='NPHI:Q',  
    #y=('RHOB'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='RHOB:Q', 
).properties(
    title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250,
    selection=interval
)

pef_chart = alt.Chart(df_pef).mark_line().encode(
    alt.X('PEF_chart:Q',
        scale=alt.Scale(domain=(0, 10))
    ),    
    alt.Y('RHOB_chart:Q',
        scale=alt.Scale(domain=(3, 2))
    ),    
    color=alt.condition(interval, 'Lith:O', alt.value('black'),scale=alt.Scale(scheme='sinebow'),legend=None),
    #color=alt.value('black'),
).properties(
    #title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250
    #selection=interval
)



pef_chart2 = alt.Chart(df_pef).mark_line().encode(
    alt.X('PEF_chart:Q',
        scale=alt.Scale(domain=(0, 10))
    ),    
    alt.Y('RHOB_chart:Q',
        scale=alt.Scale(domain=(3, 2))
    ),    
    color=alt.condition(interval, 'Por:O', alt.value('black'),scale=alt.Scale(scheme='rainbow'),legend=None),
    #color=alt.value('black'),
).properties(
    #title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250
    #selection=interval
)

pefxplot = base.mark_circle(size=20).encode(
    alt.X('PEF:Q',
        scale=alt.Scale(domain=(0, 10))
    ),    
    alt.Y('RHOB:Q',
        scale=alt.Scale(domain=(3, 2))
    ),    
    #x='NPHI:Q',  
    #y=('RHOB'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='PEF:Q', 
).properties(
    title='PEF-RHOB Xplot',
    width=250,
    height=250,
    selection=interval
)

 
pickett_chart = alt.Chart(df_pickett).mark_line(clip=True, size=2 ,strokeDash=[5,5]  ).encode(
    alt.X('Rt_Pickett:Q',
        scale=alt.Scale(type='log',domain=(.01, 100))
    ),    
    alt.Y('Por_at_Ro:Q',
        scale=alt.Scale(type='log',domain=(0.05, 1.0))
    ),    
    #color=alt.condition(interval, 'Lith:O', alt.value('black'),scale=alt.Scale(scheme='sinebow')),
    color=alt.value('blue'),
).properties(
    #title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250
    #selection=interval
)

pickett_chart8 = alt.Chart(df_pickett).mark_line(clip=True, size=2 ,strokeDash=[5,5]).encode(
    alt.X('Rt_Pickett:Q',
        scale=alt.Scale(type='log',domain=(.01, 100))
    ),    
    alt.Y('Por_at_0pt75:Q',
        scale=alt.Scale(type='log',domain=(0.05, 1.0))
    ),    
    #color=alt.condition(interval, 'Lith:O', alt.value('black'),scale=alt.Scale(scheme='sinebow')),
    color=alt.value('cyan'),
).properties(
    #title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250
    #selection=interval
)
pickett_chart6 = alt.Chart(df_pickett).mark_line(clip=True, size=2 ,strokeDash=[5,5]  ).encode(
    alt.X('Rt_Pickett:Q',
        scale=alt.Scale(type='log',domain=(.01, 100))
    ),    
    alt.Y('Por_at_0pt5:Q',
        scale=alt.Scale(type='log',domain=(0.05, 1.0))
    ),    
    #color=alt.condition(interval, 'Lith:O', alt.value('black'),scale=alt.Scale(scheme='sinebow')),
    color=alt.value('yellow'),
).properties(
    #title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250
    #selection=interval
)
pickett_chart4 = alt.Chart(df_pickett).mark_line(clip=True, size=2 ,strokeDash=[5,5]  ).encode(
    alt.X('Rt_Pickett:Q',
        scale=alt.Scale(type='log',domain=(.01, 100))
    ),    
    alt.Y('Por_at_0pt25:Q',
        scale=alt.Scale(type='log',domain=(0.05, 1.0))
    ),    
    #color=alt.condition(interval, 'Lith:O', alt.value('black'),scale=alt.Scale(scheme='sinebow')),
    color=alt.value('orange'),
).properties(
    #title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250
    #selection=interval
)
pickett_chart2 = alt.Chart(df_pickett).mark_line(clip=True , size=2 ,strokeDash=[5,5] ).encode(
    alt.X('Rt_Pickett:Q',
        scale=alt.Scale(type='log',domain=(.01, 100))
    ),    
    alt.Y('Por_at_0pt1:Q',
        scale=alt.Scale(type='log',domain=(0.05, 1.0))
    ),    
    #color=alt.condition(interval, 'Lith:O', alt.value('black'),scale=alt.Scale(scheme='sinebow')),
    color=alt.value('red'),
).properties(
    #title='Neut-Den Xplot with GR on Color Axis',
    width=250,
    height=250
    #selection=interval
)
pickett = base.mark_circle(size=20).encode(
    alt.X('ILD:Q',
        scale=alt.Scale(type='log',domain=(.01, 100))
    ),    
    alt.Y('PHIX:Q',
        scale=alt.Scale(type='log',domain=(.05, 1))
    ),    
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='ILD:Q', 
).properties(
    title='Pickett Plot with GR on Color Axis',
    width=250,
    height=250,
    selection=interval
)

nmr = base.mark_circle(size=20).encode(
    alt.X('FFI:Q',
        scale=alt.Scale(domain=(0, .4))
    ),    
    alt.Y('MPHI:Q',
        scale=alt.Scale(domain=(0, .5))
    ),    
    #x='NPHI:Q',  
    #y=('RHOB'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='FFI:Q', 
).properties(
    title='FFI vs. MPHI: Select Porosity Cutoff',
    width=250,
    height=250,
    selection=interval
)

line1 = nmr.transform_regression('MFFI:Q', 'MPHI:Q').mark_line()

cbw = base.mark_circle(size=20).encode(
    alt.X('VSH:Q',
        scale=alt.Scale(domain=(0,1))
    ),    
    alt.Y('CBW:Q',
        scale=alt.Scale(domain=(0, 1))
    ),    
    #x='NPHI:Q',  
    #y=('RHOB'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip= 'CBW:Q', 
).properties(
    title='Vsh vs. CBW',
    width=250,
    height=250,
    selection=interval
)

mna = base.mark_circle(size=20).encode(
    alt.X('VSH:Q',
        scale=alt.Scale(domain=(0, 1))
    ),    
    alt.Y('MNA:Q',
        scale=alt.Scale(domain=(0, 7))
    ),    
    #x='NPHI:Q',  
    #y=('RHOB'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
    tooltip='MNA:Q', 
).properties(
    title='Vsh vs. Apparent m*',
    width=250,
    height=250,
    selection=interval
)



grhist = alt.Chart(df).mark_bar().encode(
    alt.X("GR:Q", bin=alt.Bin(maxbins=75)),
    y='count()',
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),    
).properties(
    title='GR Hist',
    width=250,
    height=250,
    selection=interval
)

rhobhist = alt.Chart(df).mark_bar().encode(
    alt.X("RHOB:Q", bin=alt.Bin(maxbins=75)),
    y='count()',
    #color=alt.value('red'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
).properties(
    title='RHOB Hist',
    width=250,
    height=250,
    selection=interval
)

nphihist = alt.Chart(df).mark_bar().encode(
    alt.X("NPHI:Q", bin=alt.Bin(maxbins=75)),
    y='count()',
    #color=alt.value('green'),
    color=alt.condition(interval, 'GR:Q', alt.value('lightgray'),scale=alt.Scale(scheme='rainbow'),legend=None),
).properties(
    title='NPHI Hist',
    width=250,
    height=250,
    selection=interval
)

depth = gr | rhob | nphi | rt | phit | mphi | mbvi 

xplot = ndxplot+nd_chart+nd_chart2| pefxplot+pef_chart+pef_chart2 |pickett+pickett_chart+pickett_chart8+pickett_chart6+pickett_chart4  

ws = nmr | cbw | mna

hist =  grhist | rhobhist | nphihist

plot = depth & xplot & ws & hist

plot.show()  


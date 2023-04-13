import pickle
import numpy as np
import plotly.express as px
import plotly.io as io
from numba import jit, prange
from scipy.stats import poisson, binom
import matplotlib.pyplot as plt

data = pickle.load(open("20-23.p", "rb"))

names = pickle.load(open("names_20-23.p", "rb"))
size1 = 100000
for i in range(46):
    df = poisson.rvs(mu =(data[i,3]/data[i,0]),size=size1)
    fig = px.histogram(df,histnorm='probability',title=names[i])
    fig.show()
    df = binom.rvs(1000, p = ( data[i,2]/data[i,4]), size = size1)/1000
    fig = px.histogram(df,histnorm='probability',title=names[i])
    fig.show()


    
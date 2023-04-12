import pickle
import numpy as np
import plotly.express as px
import plotly.io as io
from numba import jit, prange
import csv 
with open("20-21.csv", "r", newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    
    next(spamreader)
    next(spamreader)
    i = 0
    last_season = np.zeros([32,5])
    for row in spamreader:
        last_season[i] = [row[3],row[9],row[10],row[27],row[29]]
        i +=1
        #print(row[3],row[9],row[10],row[27],row[29])
        


print(last_season)
pickle.dump(last_season, open("20-21.p", "wb"))
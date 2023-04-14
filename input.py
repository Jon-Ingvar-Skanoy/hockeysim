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
    print()
    i = 0
    last_season = np.zeros([33,5])
    names = []
    for row in spamreader:
        names.append(row[1])
        print(row[1])
        last_season[i] = [row[3],row[9],row[10],row[27],row[29]]
        i +=1
        #print(row[3],row[9],row[10],row[27],row[29])
        


print(names)
#pickle.dump(last_season, open("21-22.p", "wb"))
#pickle.dump(names, open("names_21-22.p", "wb"))
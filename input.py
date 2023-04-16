import pickle
import numpy as np
import plotly.express as px
import plotly.io as io
from numba import jit, prange
import csv 
with open("10-11.csv", "r", newline='') as csvfile: # first we determine how many lines/teams are in the file
    spamreader = csv.reader(csvfile)
    next(spamreader)
    next(spamreader)
   
    i = 0
    last_season = np.zeros([ sum(1 for row in spamreader) ,5])
with open("10-11.csv", "r", newline='') as csvfile: # then we import the file
    spamreader = csv.reader(csvfile)

    next(spamreader)
    next(spamreader)
    names = []
    for row in spamreader:
        row[1] = row[1].replace("*","")
        names.append(row[1])
        print(row[1])
        last_season[i] = [row[3],row[9],row[10],row[27],row[29]]
        i +=1
        # games played = row[3], Goals = row[9], Goals against = row[10], Shots = row[27], Shots against row[29]
          



pickle.dump(last_season, open("10-11.p", "wb"))
pickle.dump(names, open("names_10-11.p", "wb"))
print(names)
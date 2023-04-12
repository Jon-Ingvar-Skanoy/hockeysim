import pickle
import numpy as np
import plotly.express as px
import plotly.io as io
from numba import jit, prange

s1 = pickle.load(open("20-21.p", "rb"))
s2 = pickle.load(open("21-22.p", "rb"))
s3 = pickle.load(open("22-23.p", "rb"))

n1 = pickle.load(open("names_20-21.p", "rb"))
n2 = pickle.load(open("names_21-22.p", "rb"))
n3 = pickle.load(open("names_22-23.p", "rb"))
new_names = []
for row in n1:
    new_names.append(row)
for row in n2:
    if(row not in new_names):
        new_names.append(row)
for row in n3:
    if(row not in new_names):
        new_names.append(row)
#print(new_names, len(new_names))
new_array = np.zeros([len(new_names)-1,5])
for i in range(0,len(new_names)-1):
    for i2 in range(0,len(n1)):
        if(new_names[i] == n1[i2]):
            new_array[i] += s1[i2]
    for i2 in range(0,len(n2)):
        if(new_names[i] == n2[i2]):
            new_array[i] += s2[i2]
    for i2 in range(0,len(n3)):
        if(new_names[i] == n3[i2]):
            new_array[i] += s3[i2]
print(new_array)
pickle.dump(new_array, open("20-23.p", "wb"))
pickle.dump(new_names, open("names_20-23.p", "wb"))
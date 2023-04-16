import pickle
import numpy as np
import plotly.express as px
import plotly.io as io
from numba import jit, prange

old_data = []
old_names = []
# først samles den gamle listene til en liste med listene
old_data.append(pickle.load(open("22-23.p", "rb")))
old_data.append(pickle.load(open("22-23.p", "rb")))
old_data.append(pickle.load(open("21-22.p", "rb")))
old_data.append(pickle.load(open("20-21.p", "rb")))
old_data.append(pickle.load(open("19-20.p", "rb")))
old_data.append(pickle.load(open("18-19.p", "rb")))
old_data.append(pickle.load(open("17-18.p", "rb")))
old_data.append(pickle.load(open("16-17.p", "rb")))
old_data.append(pickle.load(open("15-16.p", "rb")))
old_data.append(pickle.load(open("14-15.p", "rb")))
old_data.append(pickle.load(open("13-14.p", "rb")))
old_data.append(pickle.load(open("12-13.p", "rb")))
old_data.append(pickle.load(open("11-12.p", "rb")))
old_data.append(pickle.load(open("10-11.p", "rb")))

old_names.append(pickle.load(open("names_22-23.p", "rb")))
old_names.append(pickle.load(open("names_21-22.p", "rb")))
old_names.append(pickle.load(open("names_20-21.p", "rb")))
old_names.append(pickle.load(open("names_19-20.p", "rb")))
old_names.append(pickle.load(open("names_18-19.p", "rb")))
old_names.append(pickle.load(open("names_17-18.p", "rb")))
old_names.append(pickle.load(open("names_16-17.p", "rb")))
old_names.append(pickle.load(open("names_15-16.p", "rb")))
old_names.append(pickle.load(open("names_14-15.p", "rb")))
old_names.append(pickle.load(open("names_13-14.p", "rb")))
old_names.append(pickle.load(open("names_12-13.p", "rb")))
old_names.append(pickle.load(open("names_11-12.p", "rb")))
old_names.append(pickle.load(open("names_10-11.p", "rb")))

new_names = []
# lager en liste med alle navn i alle sesongene
for n in old_names:
    for row in n:
        row = row.replace("*","")
        if(row not in new_names):
            new_names.append(row)
      
  
print(new_names, len(new_names))
new_array = np.zeros([len(new_names),5])
# går gjennom alle nye navn og alle sesonger adderer opp all data for hvert enkelt lag. 
for i in range(0,len(new_names)):
    for year in range(len(old_names)):
        for i2 in range(0,len(old_names[year])):
            old_names[year][i2]= old_names[year][i2].replace("*","")
            if(new_names[i] == old_names[year][i2]):
                new_array[i] += (old_data[year][i2]*(1-year/20)).round()

# loop som som printer alle navn med tilhørende data
for i in range(33):
   print(new_names[i], new_array[i])

# lager pickle filer med den samlede dataen
pickle.dump(new_array, open("20-23.p", "wb"))
pickle.dump(new_names, open("names_20-23.p", "wb"))
import pandas as pd #Pandas dataframs
import numpy as np #Numpy arrays
import matplotlib.pyplot as plt #Visualization 
from scipy import stats
from sklearn.metrics import r2_score #Scoring the model
import seaborn as sns 


df = pd.read_csv('data.csv')
df.columns = ['index', 'distance', 'intensity']

plt.figure(figsize=(10,6), dpi=80)
plt.scatter(df.distance, df.intensity)
plt.xlabel('Distance from object in mm')
plt.ylabel('Pixel Intenisty of object in field of Concern')
plt.savefig('Scatter-Plot.png')
plt.show()


slope, intercept, r_value, p_value, std_err = stats.linregress(df.distance, df.intensity)
print("SLOPE: " + str(slope))
print("INTERCEPT: " + str(intercept))
print("R_VALUE: " + str(r_value))
print("P_VALUE: " + str(p_value))
print("STD_ERR: " + str(std_err))

ax = sns.regplot(x = df.distance, y = df.intensity, data = df)
plt.savefig('Linear_reg.png')
plt.show()
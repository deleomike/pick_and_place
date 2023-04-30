import pandas as pd
import numpy as np
from matplotlib import pyplot as plt 
from matplotlib.animation import FuncAnimation 

# import updated variables from state_machine.py
from state_machine import number_good_pickup, number_bad_pickup, number_good_place, number_bad_place


# use exec(open('metrics.py').read()) in the state_machine while loop to call this function

# make dataframe from variables and exporting to excel
df = pd.DataFrame(columns = ['Pickup Success', 'Pickup Fail', 'Pickup Attempts', 'Place Success', 'Place Fail', 'Place Attempts'])
df.loc[len(df)] = [number_good_pickup, number_bad_pickup, number_good_pickup+number_bad_pickup, number_good_place, number_bad_place, number_good_place+number_bad_place]

# name the file
file_name = 'Group1_Metrics.xlsx'
  
# saving the file to excel
df.to_excel(file_name)

# create labels and nukmbers list for pie chart
labels = ['Pickup Success', 'Pickup Fail', 'Place Success', 'Place Fail']
nums = [number_good_pickup, number_bad_pickup, number_good_place, number_bad_place]

# create pie chart object
fig,ax = plt.subplots()

# function to create objects on pie chart
def animate(i):
    ax.clear()
    ax.axis('equal')
    ax.pie(nums, labels=labels, shadow=True, startangle=140) 

# iterate pie chart as values change
anim = FuncAnimation(fig, animate, frames=100, repeat=False) 

# show pie chart figure
plt.show()



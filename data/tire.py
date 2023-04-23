import csv
import matplotlib.pyplot as plt
import random as r
import numpy as np
r.seed(420)
pressure = 35
p_left = []
days = []
d = 0
while(d<=30):
    p_drop = r.randint(3,8)/10
    pressure = pressure - p_drop if pressure - p_drop>=25 else 25 
    p_left.append(pressure)
    d += 1  
    days.append(d)
data = []
with open('/home/varun/mqtt/data/tire.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for i in range(len(p_left)):
        data = [days[i],p_left[i]]
        writer.writerow(data)
'''
x = np.array(days)
y = np.array(p_left) 
fig, ax = plt.subplots()
mngr = plt.get_current_fig_manager()
mngr.canvas.manager.window.setGeometry(1500, 100,250,250)
ax.plot(x,y)
plt.ylim(23,35)
plt.xlabel('Days')
plt.ylabel('Tire Pressure(psi)')
plt.title('Tire Pressure wrt Time')
plt.show()
'''
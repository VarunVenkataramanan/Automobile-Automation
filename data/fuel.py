import csv
import matplotlib.pyplot as plt
import matplotlib
import random as r
import numpy as np
r.seed(420)
fuel = 50.0
eng_cap = 1.6
rpm = 800
fuel_cons = 0.00185 * eng_cap * 0.346 * rpm #0.8193280000000001
f_left = []
days = []
d = 0
while(fuel>0):
    a = (r.randint(0,200)/100)
    b = (r.randint(0,200)/100)
    l = r.choices(population=[[0.00185 * (eng_cap+a*eng_cap) * 0.346 * (rpm+b*rpm)],[0]],weights = [0.6,0.4])
    fuel_cons = l[0][0]
    fuel = fuel - fuel_cons if fuel - fuel_cons>=0 else 0 
    f_left.append(fuel)
    d += 1
    days.append(d)
data = []
with open('/home/varun/mqtt/data/fuel.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for i in range(len(f_left)):
        data = [days[i],f_left[i]]
        writer.writerow(data)
'''
x = np.array(days)
y = np.array(f_left) 
fig, ax = plt.subplots()
mngr = plt.get_current_fig_manager()
mngr.canvas.manager.window.setGeometry(545, 100,250,250)
ax.plot(x,y)
plt.ylabel('Fuel Consumed')
plt.xlabel('Days')
plt.title('Fuel Consumed wrt Time')
plt.show()
'''

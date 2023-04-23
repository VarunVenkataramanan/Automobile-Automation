import matplotlib.pyplot as plt
import random as r
import numpy as np
import math as m
import csv
r.seed(69) #106,3,6 8743,1,9 69,2
xmin = 85
width = 2
def sin1(x,n):
    y_l = []
    for i,j in zip(x,n):
        y_p = 100*abs(m.sin(i/width)/3) + j
        y_l.append(y_p+xmin)
    return y_l
def sin2(x,n):
    y_l = []
    for i,j in zip(x,n):
        y_p = 100*abs(m.sin(i/width)/6  ) + j
        y_l.append(y_p+xmin)
    return y_l
xi = np.zeros(100)
x = np.zeros(0)
sens = [sin1, sin2]
f = 0
xc = 0
yc = 0
y_l =[]
while(f<=30):
    n = np.random.normal(scale = 4,size = xi.size)
    xi = np.linspace(f,f+width*np.pi,num = 100)
    x = np.append(x,xi,0)
    y_axes = (r.choices(population=sens,weights=[0.1,0.9])[0])(xi,n)
    y_l.extend(y_axes)
    xc += len(xi)
    yc += len(y_axes)
    f += width*np.pi
y = np.array(y_l)
'''
fig, ax = plt.subplots()
mngr = plt.get_current_fig_manager()
mngr.canvas.manager.window.setGeometry(545, 500,250,250)
ax.plot(x,y)
yTicks = np.arange(80,200,10)
plt.yticks(yTicks)
plt.xlim([0,30])
plt.ylim([70,200])
plt.xlabel('Hours')
plt.ylabel('Temperature')
plt.title('Change in Engine Temperature wrt Time')
plt.show()
'''
x = list(x)
data = []
with open('/home/varun/mqtt/data/engine.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for i in range(len(y)):
        data = [x[i],y[i]]
        writer.writerow(data)
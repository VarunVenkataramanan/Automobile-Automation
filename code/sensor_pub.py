#Import necessary modules
import csv
import nacl
from nacl.public import PrivateKey, Box,PublicKey
import time
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import threading
import matplotlib.pyplot as plt
import numpy as np

#Generate a Private Key and Public Key for PUBLISHER
p_private = PrivateKey.generate()
p_public = p_private.public_key.encode(encoder=nacl.encoding.Base64Encoder)

#Publish the PUBLISHER's Public Key
publish.single("public",p_public)
print('sending p_public to all')

#Recieve the Public Keys of all 3 SUBSCRIBERS
msg1 = subscribe.simple("s1")
msg1 = msg1.payload.decode("utf-8")
s1_public = PublicKey(msg1,encoder=nacl.encoding.Base64Encoder)
print('receiving s1_public from s1')
msg2 = subscribe.simple("s2")
msg2 = msg2.payload.decode("utf-8")
s2_public = PublicKey(msg2,encoder=nacl.encoding.Base64Encoder)
print('receiving s2_public from s2')
msg3 = subscribe.simple("s3")
msg3 = msg3.payload.decode("utf-8")
s3_public = PublicKey(msg3,encoder=nacl.encoding.Base64Encoder)
print('receiving s3_public from s3')

#Create Box variables for all 3 SUBSCRIBERS
s1_box = Box(p_private,s1_public)
s2_box = Box(p_private,s2_public)
s3_box = Box(p_private,s3_public)

#Connect all 3 CLIENTS to the BROKER
broker="localhost"
topic1 = "Fuel"
topic2 = "Tire"
topic3 = "Engine"
client1= paho.Client("client-001") 
client2= paho.Client("client-002") 
client3= paho.Client("client-003") 
print("connecting to broker ",broker)
client1.connect(broker,1883,60)
client2.connect(broker,1883,60)
client3.connect(broker,1883,60)
print("publishing ")

#Read data from CSV files
x1=[]
y1=[]
x2=[]
y2=[]
x3=[]
y3=[]
with open('/home/varun/mqtt/data/fuel.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        xi = float(lines[0])
        yi = float(lines[1])
        x1.append(xi)
        y1.append(yi)
with open('/home/varun/mqtt/data/tire.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        xi = float(lines[0])
        yi = float(lines[1])
        x2.append(xi)
        y2.append(yi)
with open('/home/varun/mqtt/data/engine.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        xi = float(lines[0])
        yi = float(lines[1])
        x3.append(xi)
        y3.append(yi)

#Publish the appropriate data to their respective TOPICS
def s1(y):
    for i in y:
        s = str(i)
        x = s.encode('utf-8')
        enc_msg = s1_box.encrypt(x)
        client1.publish(topic1,enc_msg)
        time.sleep(0.5)
streaming_thread1= threading.Thread(target=s1,args = (y1,))
streaming_thread1.start()
def s2(y):
    for i in y:
        s = str(i)
        x = s.encode('utf-8')
        enc_msg = s2_box.encrypt(x)
        client2.publish(topic2,enc_msg)
        time.sleep(0.5)
streaming_thread2= threading.Thread(target=s2,args = (y2,))
streaming_thread2.start()
def s3(y):
    for i in y:
        s = str(i)
        x = s.encode('utf-8')
        enc_msg = s3_box.encrypt(x)
        client3.publish(topic3,enc_msg)
        time.sleep(0.1)
streaming_thread3= threading.Thread(target=s3,args = (y3,))
streaming_thread3.start()

#Plot the respective datas
x1 = np.array(x1)
y1 = np.array(y1)
mngr = plt.get_current_fig_manager()
mngr.canvas.manager.window.setGeometry(1500, 100,250,250)
plt.plot(x1,y1,marker = '.',mfc = 'r',ms = 6)
plt.ylabel('Fuel Consumed')
plt.xlabel('Days')
fig = plt.gcf()
fig.canvas.manager.set_window_title('Fuel Consumed wrt Time')
plt.figure()
x2 = np.array(x2)
y2 = np.array(y2)
mngr = plt.get_current_fig_manager()
mngr.canvas.manager.window.setGeometry(545, 500,250,250)
plt.plot(x2,y2,marker = '.',mfc = 'r',ms = 6)
plt.xlabel('Days')
plt.ylabel('Tire Pressure(psi)')
fig = plt.gcf()
fig.canvas.manager.set_window_title('Tire Pressure wrt Time')
plt.figure()
x3 = np.array(x3)
y3 = np.array(y3)
mngr = plt.get_current_fig_manager()
mngr.canvas.manager.window.setGeometry(1500, 500,250,250)
plt.plot(x3,y3)
plt.xlabel('Hours')
plt.ylabel('Temperature')
fig = plt.gcf()
fig.canvas.manager.set_window_title('Engine Temperature wrt Time')

plt.show()

#Join all threads
streaming_thread1.join()
streaming_thread2.join()
streaming_thread3.join()

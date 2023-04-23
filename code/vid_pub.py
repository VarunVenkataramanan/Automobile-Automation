#Import necessary modules
import cv2
import nacl
from nacl.public import PrivateKey, Box,PublicKey
import time
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import threading

time.sleep(2)

#Generate a Private Key and Public Key for PUBLISHER
u1_private = PrivateKey.generate()
u1_public = u1_private.public_key.encode(encoder=nacl.encoding.Base64Encoder)

#Publish the PUBLISHER's Public Key
publish.single("public",u1_public)
print('sending u1_public to u2')

#Recieve the Public Key of the SUBSCRIBER
msg = subscribe.simple("public")
msg = msg.payload.decode("utf-8")
u2_public = PublicKey(msg,encoder=nacl.encoding.Base64Encoder)
print('receiving u2_public from u2')

#Create a Box variables
u1_box = Box(u1_private,u2_public)

#Connect the CLIENT to the BROKER
host = "127.0.0.1"
port = 1883
topic = "vid"
client3= paho.Client("client-003") 
client3.connect(host, port)

#Capture video from laptop camera (Interface 0)
cam = cv2.VideoCapture(0)  

#Encrypt the data using the Box before publishing it
def encrypt(data):
    enc_msg = u1_box.encrypt(data)
    client3.publish(topic,enc_msg)

#Publish the video stream generated
def stream():
    print("Streaming from video source : 0")
    while True:
        #Convert the image frame to bytes
        _ , img = cam.read()
        img_str = cv2.imencode('.jpg', img)[1].tobytes()
        #Thread the encrypt function to make the video appear smooth
        enc = threading.Thread(target=encrypt,args=(img_str,))
        enc.start()

#Thread the stream function to make the video appear smooth
streaming_thread= threading.Thread(target=stream)
streaming_thread.start()
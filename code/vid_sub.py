#Import necessary modules
import cv2
import numpy as np
import nacl
from nacl.public import PrivateKey, PublicKey, Box
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

#Generate a Private Key and Public Key for SUBSCRIBER
u2_private = PrivateKey.generate()
u2_public = u2_private.public_key.encode(encoder=nacl.encoding.Base64Encoder)

#Recieve the Public Key of the PUBLISHER
msg = subscribe.simple("public")
msg = msg.payload.decode("utf-8")
u1_public = PublicKey(msg,encoder=nacl.encoding.Base64Encoder)
print('receiving u1_public from u1')

#Publish the SUBSCRIBER's Public Key
publish.single("public",u2_public)
print('sending u2_public to u1')

#Create a Box variable
u2_box = Box(u2_private, u1_public)
      
#CALLBACK function to subscribe to the topic when the client connects to the broker
def on_connect(client, _, __,___): 
    client.subscribe(topic)
    print("Subscribing to topic:", topic)

#CALLBACK function to convert the decrypted bytes to frames
def on_message(_, __, msg):
    enc_msg = msg.payload
    plaintext = u2_box.decrypt(enc_msg)
    nparr = np.frombuffer(plaintext, np.uint8)
    frame = cv2.imdecode(nparr,  cv2.IMREAD_COLOR)
    cv2.imshow('recv', frame)
    cv2.waitKey(1)

#Connect the CLIENT to the BROKER
topic = "vid"
host = "127.0.0.1"
port = 1883
frame = None
client4= paho.Client("client-004") 
client4.on_connect = on_connect
client4.message_callback_add(topic,on_message)
client4.connect(host,port)
client4.loop_forever() 
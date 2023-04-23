#Import necessary modules
import nacl
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from nacl.public import PrivateKey, PublicKey, Box

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
def on_connect(client, _, __, ___): 
    client.subscribe(topic)
    print("Subscring to topic :",topic)

#CALLBACK function to convert the decrypted bytes to frames
def on_message(_, __, msg):
    plaintext = u2_box.decrypt(msg.payload)
    plaintext = plaintext.decode()
    print(plaintext)

#Connect the CLIENT to the BROKER
topic = "sleep"
host = "127.0.0.1"
port = 1883
frame=None
client6= paho.Client("client-006") 
client6.on_connect = on_connect
client6.on_message = on_message
client6.connect(host,port)
client6.subscribe(topic)
client6.loop_forever()
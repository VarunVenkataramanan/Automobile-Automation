#Import necessary modules
import time
import nacl
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from nacl.public import PrivateKey, PublicKey, Box

#Generate a Private Key and Public Key for SUBSCRIBER_2
s2_private = PrivateKey.generate()
s2_public = s2_private.public_key.encode(encoder=nacl.encoding.Base64Encoder)

#Subscribe to recieve PUBLISHER's Public Key
msg = subscribe.simple("public")
msg = msg.payload.decode("utf-8")
p_public = PublicKey(msg,encoder=nacl.encoding.Base64Encoder)
print('receiving p_public from u1')
time.sleep(1)

#Publish the SUBSCRIBER_2's Public Key
publish.single("s2",s2_public)
print('sending s2_public to u1')

#Create a Box variable
u2_box = Box(s2_private, p_public)

#CALLBACK function to print the decrypted messages whenever it receives it
def on_message(client, userdata, message):
    enc_msg = message.payload
    plaintext = u2_box.decrypt(enc_msg)
    plaintext = float(plaintext)
    if (plaintext<=27):
        print('LOW TIRE PRESSURE: ',str(plaintext))

#Connect the CLIENT to the BROKER
broker="localhost"
topic = "Tire"
client5= paho.Client("client-005") 
client5.on_message=on_message
print("connecting to broker ",broker)
client5.connect(broker,1883,60)
print("subscribing ")
client5.subscribe(topic)
client5.loop_forever()
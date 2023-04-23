#Import necessary modules
import time
import nacl
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from nacl.public import PrivateKey, PublicKey, Box

#Generate a Private Key and Public Key for SUBSCRIBER_3
s3_private = PrivateKey.generate()
s3_public = s3_private.public_key.encode(encoder=nacl.encoding.Base64Encoder)

#Subscribe to recieve PUBLISHER's Public Key
msg = subscribe.simple("public")
msg = msg.payload.decode("utf-8")
p_public = PublicKey(msg,encoder=nacl.encoding.Base64Encoder)
print('receiving p_public from u1')
time.sleep(2)

#Publish the SUBSCRIBER_3's Public Key
publish.single("s3",s3_public)
print('sending s3_public to u1')

#Create a Box variable
u2_box = Box(s3_private, p_public)

#CALLBACK function to print the decrypted messages whenever it receives it
def on_message(_, __, message):
    enc_msg = message.payload
    plaintext = u2_box.decrypt(enc_msg)
    plaintext = float(plaintext)
    if (plaintext>=115):
        print('HIGH ENGINE TEMPERATURE: ',str(plaintext))

#Connect the CLIENT to the BROKER
broker="localhost"
topic = "Engine"
client6= paho.Client("client-006") 
client6.on_message=on_message
print("connecting to broker ",broker)
client6.connect(broker,1883,60)
print("subscribing ")
client6.subscribe(topic)
client6.loop_forever()
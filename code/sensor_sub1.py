#Import necessary modules
import nacl
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from nacl.public import PrivateKey, PublicKey, Box

#Generate a Private Key and Public Key for SUBSCRIBER_1
s1_private = PrivateKey.generate()
s1_public = s1_private.public_key.encode(encoder=nacl.encoding.Base64Encoder)

#Subscribe to recieve PUBLISHER's Public Key
msg = subscribe.simple("public")
msg = msg.payload.decode("utf-8")
p_public = PublicKey(msg,encoder=nacl.encoding.Base64Encoder)
print('receiving p_public from u1')

#Publish the SUBSCRIBER_1's Public Key
publish.single("s1",s1_public)
print('sending s1_public to u1')

#Create a Box variable
u2_box = Box(s1_private, p_public)

#CALLBACK function to print the decrypted messages whenever it receives it
def on_message(_, __, message):
    enc_msg = message.payload
    plaintext = u2_box.decrypt(enc_msg)
    plaintext = float(plaintext)
    if (plaintext<=10):
        print('LOW FUEL: ',str(plaintext))

#Connect the CLIENT to the BROKER
broker="localhost"
topic = "Fuel"
client4= paho.Client("client-004") 
client4.on_message=on_message
print("connecting to broker ",broker)
client4.connect(broker,1883,60)
print("subscribing ")
client4.subscribe(topic)
client4.loop_forever()
#Import necessary modules
from scipy.spatial import distance
from imutils import face_utils
import imutils
import time
import dlib
import cv2
import nacl
from nacl.public import PrivateKey, Box,PublicKey
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

#Create a Box variable
u1_box = Box(u1_private,u2_public)

#Connect the CLIENT to the BROKER
host = "127.0.0.1"
port = 1883
topic = "sleep"
cap=cv2.VideoCapture(0)
client5 = paho.Client("client-005") 
client5.connect(host, port)

#Function to calculate Eye Aspect Ratio
def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
	
#Function to Encrypt the data and Publish it
def encrypt(data):
    data = data.encode('utf-8')
    enc_msg = u1_box.encrypt(data)
    client5.publish(topic,enc_msg)

#Function to decide state of the driver
def alert():
    state = 'alert'
    thresh = 0.25
    frame_check = 30

    #Predict the 68 Facial Landmarks using a pre-trained model
    detect = dlib.get_frontal_face_detector()
    predict = dlib.shape_predictor("/home/varun/mqtt/data/shape_predictor_68_face_landmarks.dat")

    #Get the Indices for the points related to left and right eye
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
    
    flag=0
    while True:
        _ , frame=cap.read()
        frame = imutils.resize(frame, width=550)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #Creates a boundary around a detected face
        subjects = detect(gray, 0)
        for subject in subjects:
            state = 'alert'
            #Predicts the facial Landmark
            shape = predict(gray, subject)
            #Converting to NumPy Array
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            #Calculate EAR ratio
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            #Draw Contours around the eye
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            #Change driver's state
            if ear < thresh:
                flag += 1
                if flag >= frame_check:
                    state = 'sleepy'
            else:
                flag = 0
            #Thread the encrypt function to make the video appear smooth
            enc = threading.Thread(target=encrypt,args=(state,))
            enc.start()
        #Generate the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    cap.release() 

streaming_thread= threading.Thread(target=alert)
streaming_thread.start()
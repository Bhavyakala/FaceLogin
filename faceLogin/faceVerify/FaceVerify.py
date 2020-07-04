import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.models import load_model
import cv2
import dlib
from scipy.spatial.distance import cosine
import argparse
import face_recognition

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imageFile", required=True, help="image for verification")

args = vars(ap.parse_args())

im1 = cv2.imread(args['imageFile'])
model = load_model('dl_models/facenet_keras.h5')
model.load_weights('dl_models/facenet_keras_weights.h5')
net = cv2.dnn.readNetFromCaffe("dl_models/deploy.prototxt.txt", "dl_models/res10_300x300_ssd_iter_140000.caffemodel")

def get_encoding(frame, net,model) :
    (h,w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (256,256)), 1.0, (256, 256), (104.0, 117.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    startX=0
    startY=0
    endX=0
    endY=0
    for i in range(0,detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence < 0.7:
            continue    
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        image = frame[startY-1:endY-1, startX+1:endX+1]
        face = cv2.resize(image,(160,160))
        roi = face.astype("float") / 255.0
        roi = np.reshape(roi,(1,160,160,3))
        encoding = model.predict(roi)
    im = cv2.rectangle(frame.copy(),(startX,startY),(endX,endY),(255,0,0),2)
    return encoding,im, image

cap = cv2.VideoCapture(0)
while True:
    _,frame = cap.read()
    enc1,_,im2 = get_encoding(im1,net,model)
    enc2, im,_ = get_encoding(frame,net,model)
    score = cosine(enc1,enc2)
    if score  <= 0.5 :
        print(True)
    else :
        print(False)
    cv2.imshow('image',im)
    cv2.imshow("groundTruth", im2)
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break
cv2.destroyAllWindows()
cap.release()
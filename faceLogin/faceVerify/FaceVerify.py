import numpy as np
from keras.models import load_model
import keras
import cv2
from scipy.spatial.distance import cosine
from .utils import decode_base64
from django.conf import settings
import os
base_dir = os.path.dirname(os.path.realpath(__file__))

class FaceVerify() :

    def get_encoding(self,frame, net,model) :
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
        cv2.imwrite('im.jpg',image)
        return encoding,im, image

    def check_face_id(self, profilePicture, image) :
        model = load_model(os.path.join(base_dir,'dl_models/facenet_keras.h5'))
        model.load_weights(os.path.join(base_dir,'dl_models/facenet_keras_weights.h5'))
        net = cv2.dnn.readNetFromCaffe(os.path.join(base_dir,"dl_models/deploy.prototxt.txt"),
                                       os.path.join(base_dir,"dl_models/res10_300x300_ssd_iter_140000.caffemodel"))
        
        im1 = cv2.imread(os.path.join(settings.MEDIA_ROOT, profilePicture))
        frame = decode_base64(image)
        frame = np.frombuffer(frame, dtype=np.uint8)
        frame = cv2.imdecode(frame,flags=1)
        # print(type(frame))  
        # cv2.imwrite('im.jpg',frame)
        # frame = cv2.imread(frame)
        enc1,_,im2 = self.get_encoding(im1,net,model)
        enc2, im,_ = self.get_encoding(frame,net,model)
        score = cosine(enc1,enc2)
        print(score)
        # keras.backend.clear_session()
        if score  <= 0.5 :
            return True
        else :
            return False
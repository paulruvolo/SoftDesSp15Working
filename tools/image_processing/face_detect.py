""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('./foxnews_religion.mp4')
downsample_factor = 10
frame_count = 0
while (True):
	# capture a frame from the camera
	ret, frame = cap.read()
	if type(frame) == type(None):
		break

	frame_count += 1
	if frame_count % downsample_factor:
		continue
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
	for (x,y,w,h) in faces:
		frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)

	for (x,y,w,h) in faces:
		# draw the whites of the eyes
		cv2.circle(frame,(int(x + w*0.27), int(y + h*0.35)), int(w*0.1), (255,255,255), thickness=-1)
		cv2.circle(frame,(int(x + w*(1-0.3)), int(y + h*0.35)), int(w*0.1), (255,255,255), thickness=-1)

		# draw the pupils
		cv2.circle(frame,(int(x + w*0.27), int(y + h*0.38)), int(w*0.05), (0,0,0), thickness=-1)
		cv2.circle(frame,(int(x + w*(1-0.3)), int(y + h*0.38)), int(w*0.05), (0,0,0), thickness=-1)

		cv2.ellipse(frame, (int(x+w*0.5), int(y+h*0.75)), (int(w*0.20), int(0.07*h)), 0, 0, 180, (0,0,0), thickness=8)

	cv2.imshow('frame',frame)
	if cv2.waitKey(2) == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()
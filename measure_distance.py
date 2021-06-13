import cv2
import numpy as np
import math 



class distance:
	'''
	Calculate the distance between the circle marker and camera

	:param image: Image of object whose distance is to be measured
	:param imageCanny: Canny Image 
	:param marker_rad: Radius of circle marker
	:param focal_length: Focal length calculated at the time of callibration
	'''
    #initializes the values
    def __init__(self, image, imageCanny, marker_rad, focal_length):   
        self.image=image
        self.imageCanny=imageCanny
        self.marker_rad=marker_rad
        self.focal_length=focal_length
        self.distance=0.0

    #Return Focal length and marker radius
    def get_val(self):
        return self.focal_length, self.marker_rad


    #Calculate the distance between the marker and the camera    
    def getDistance(self):
	    contours,hierarchy = cv2.findContours(self.imageCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	    for cnt in contours:
	        area = cv2.contourArea(cnt)
	        
	        if area>500:
	            cv2.drawContours(self.image, cnt, -1, (255, 0, 0), 3)
	            peri = cv2.arcLength(cnt,True)
	            #print(peri)
	            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
	            print(len(approx))
	            objCor = len(approx)
	            x, y, w, h = cv2.boundingRect(approx)

	           
	            if objCor>4: 
	                objectType= "Circles"
	                print(f'The area of circle is:{area}')  
	                pixel_rad=math.sqrt(area/math.pi)
	                
	                
	                distance=self.focal_length*self.marker_rad/pixel_rad
	                print(f'The calculated distance is {distance}')
	            else:objectType="None"



	            cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,255,0),2)
	            cv2.putText(self.image, objectType,
	                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
	                        (0,0,0),2)
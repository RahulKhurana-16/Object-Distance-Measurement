import cv2
import numpy as np
import math 

class focalLength:
    '''
    Calculate the distance between the circle marker and camera

    :param image: Image of object whose distance is to be measured
    :param marker_rad: Radius of circle marker
    :param distance: Distance between the marker and the camera
    '''
    #initializes the values
    def __init__(self, image, distance, marker_rad):  
        self.image=image
        self.distance=distance
        self.marker_rad=marker_rad
        self.focal=0.0


    #Return distance between the marker and camera along with marker radius
    def get_val(self):
        return self.distance, self.marker_rad
    

    #Return Focal length in the pixel      
    def getFocalLength(self):
        contours,hierarchy = cv2.findContours(self.image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            
            if area>500:
                
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
                    self.focal=self.distance*pixel_rad/self.marker_rad
                    
                    
                else:objectType="None"



                
        return self.focal
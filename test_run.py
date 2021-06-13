'''
Object Distance Detection 
'''
import cv2
import numpy as np
import math 
from calibration import focalLength as fl
from measure_distance import distance

def stackImages(scale,imgArray):
    '''
    Generates a single scaled image consisting of all the image 
    
    :param scale: float, provide a value to which all the images is to be scaled 
    :param imgArray: String Array, list of images to merged 
    '''
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
#Enter the path of the train image which would be used for callibration of focal length in pixel  
train_path = 'train/calibration.jpg'
img = cv2.imread(train_path)
imgContour = img.copy()


imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)

obj=fl(imgCanny,30,2)

pix_focal=obj.getFocalLength()
print(f'The focal length in pixels is{pix_focal}')

#Enter the path of the test image whose distance is to be measured  
test_path = 'test/50.jpg'
img_test = cv2.imread(test_path)
imgCont = img_test.copy()


imgGray_test = cv2.cvtColor(img_test,cv2.COLOR_BGR2GRAY)
imgBlur_test = cv2.GaussianBlur(imgGray_test,(7,7),1)
imgCanny_test = cv2.Canny(imgBlur_test,50,50)

distanceobj=distance(imgCont,imgCanny_test,2,pix_focal)

distanceobj.getDistance()

cv2.imshow("Final output", imgCont)
cv2.waitKey(0)
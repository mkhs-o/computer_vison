import numpy as np
import cv2 as cv

img_path = 'images/mackee.jpg'
 
img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
img = cv.medianBlur(img,7)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
 
circles = cv.HoughCircles(img,
                          cv.HOUGH_GRADIENT,
                          dp = 1,
                          minDist = 100,
                          param1=50,
                          param2=60,
                          minRadius=0,
                          maxRadius=0)
if not(len(circles)):
    print("円検知不可")
    exit()

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
 # draw the outer circle
 cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
 # draw the center of the circle
 cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
 
cv.namedWindow('detected circles', cv.WINDOW_NORMAL)
cv.resizeWindow('detected circles' ,800,600)
cv.imshow('detected circles',cimg)
cv.waitKey(0)
cv.destroyAllWindows()
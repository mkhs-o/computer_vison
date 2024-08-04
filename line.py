import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = "clocks/1.png"
image= cv2.imread(image_path)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred =cv2.GaussianBlur(gray_image, (5, 5), 0)

edges = cv2.Canny(blurred, 20, 50, apertureSize = 3)    # Cannyエッジ検出
cv2.imwrite('edges.png', edges)
#計算不可が少ない、長さを決められる, maxLineGap 検出された2本の線を1本とみなす間隔
lines = cv2.HoughLinesP(edges,               
                        rho = 1,              
                        theta = np.pi/100,
                        threshold = 100,       
                        minLineLength = 15,    
                        maxLineGap = 100       # 検出された2本の線を1本とみなす
                       )
# 線分が見つかれば{x1, y1, x2, y2}のタプル、見つからなければNone
if lines is not None:
    for line in lines:
        # print(line[0])
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1) ,(x2, y2), (0, 0, 255), 10)
else:
    print("検知なし")

cv2.imwrite('line.png',image)


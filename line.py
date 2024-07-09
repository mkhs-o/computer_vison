import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = "circles/3.png"
image= cv2.imread(image_path)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('tmp.png', gray_image)
blurred =cv2.GaussianBlur(gray_image, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 159, apertureSize = 3)

#計算不可が少ない、長さを決められる, maxLineGap 検出された2本の線を1本とみなす間隔
lines = cv2.HoughLinesP(edges,               
                        rho = 1,                   # 極座標のρ
                        theta = np.pi/100,
                        threshold = 30,       # np.pi (radian)
                        minLineLength = 1,  # 
                        maxLineGap = 1  # 検出された2本の線を1本とみなす
                       )

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1) ,(x2, y2), (0, 0, 255), 2)
else:
    print("検知なし")


plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
cv2.imwrite('hough_lines/7.png', image)
plt.axis('off')
plt.show()

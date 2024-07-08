import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = 'circles/IMG_9546.jpg'
image = cv2.imread(image_path)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

# ハフ変換を使用して円を検出する, dpは解像度の比率, minDistは円の中心  同士の最小距離
circles = cv2.HoughCircles(blurred, 
                           cv2.HOUGH_GRADIENT, 
                           dp=1.5, 
                           minDist=330,     #円の中心の最小距離、誤検出に関わる
                           param1=100,      #Cannyエッジ検出の大きい方のしきい値
                           param2=40,       #投票数の基準？
                           minRadius=800,   #最小半径   
                           maxRadius=1200   #最大半径
                           )

if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    x_sum = 0
    y_sum = 0
    for (x, y, r) in circles:

        x_sum +=x
        y_sum +=y
        cv2.circle(image, (x, y), r, (0, 255, 0), 10)
        cv2.circle(image, (x, y ), 30 , (0, 255, 0), 10)
        # print(f"検出された円の中心: ({x}, {y}), 半径: {r}")
    cv2.circle(image, (x_sum//len(circles), (y_sum//len(circles))), 30, (255, 0, 0), 10)
else:
    print("円が見つかりませんでした")
# 結果を表示する
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
cv2.imwrite('hough_circles/7.png', image)
plt.axis('off')
plt.show()

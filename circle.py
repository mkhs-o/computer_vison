import cv2
import numpy as np
import os

result_dir = 'circles'
images_dir = 'clocks'

os.makedirs(result_dir, exist_ok = True)
files = os.listdir(images_dir)

for file in files:
    image_path = os.path.join(images_dir, file)
    image = cv2.imread(image_path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # ハフ変換による円を検出
    circles = cv2.HoughCircles(blurred, 
                            cv2.HOUGH_GRADIENT, 
                            dp=1.5,          # dpは解像度の比率
                            minDist=330,     # 円の中心の最小距離、誤検出に関わる
                            param1=100,      # Cannyエッジ検出の大きい方のしきい値
                            param2=40,       # 投票数の基準
                            minRadius=800,   # 最小半径   
                            maxRadius=1400   # 最大半径
                            )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        circles = circles[0, :]
        x_sum = 0
        y_sum = 0
        for (x, y, r) in circles:
            x_sum += x
            y_sum += y
            cv2.circle(image, (x, y), r, (0, 255, 0), 10)
            cv2.circle(image, (x, y ), 30 , (0, 255, 0), 10)
        x_ave = x_sum // len(circles)
        y_ave = y_sum // len(circles)
        # 円の中心座標の平均をプロット
        cv2.circle(image, (x_ave, y_ave), 30, (255, 0, 0), 20)
        image_name = file.replace('.png', '_circle.png')
        cv2.imwrite(f'{result_dir}/{image_name}', image)
    else:
        print('円未検出')




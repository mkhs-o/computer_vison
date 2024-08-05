import cv2
import numpy as np
import os

result_dir = 'lines'
images_dir = 'clocks'

os.makedirs(result_dir, exist_ok = True)
files = os.listdir(images_dir)

for file in files:
    image_path = os.path.join(images_dir, file)
    image= cv2.imread(image_path)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred =cv2.GaussianBlur(gray_image, (5, 5), 0)

    edges = cv2.Canny(blurred, 20, 50, apertureSize = 3)    # Cannyエッジ検出
    cv2.imwrite('edges.png', edges)
    # ハフ変換
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
        image_name = file.replace('.png', '_line.png')
        cv2.imwrite(f'{result_dir}/{image_name}',image)
    else:
        print("直線未検出")



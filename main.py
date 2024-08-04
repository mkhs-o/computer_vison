import cv2
import numpy as np
import matplotlib.pyplot as plt

# 直線の傾きを求める関数
# def angle(line1, line2):
#     x1_1, y1_1, x1_2, y1_2 = line1
#     x2_1, y2_1, x2_2, y2_2 = line2

#     angle1 = np.arctan2(y1_2 - y1_1, x1_2 - x1_1)
#     angle2 = np.arctan2(y2_2 - y2_1, x2_2 - x2_1)
#     angle = np.abs(angle1 - angle2)
#     return np.degrees(angle)

image_path = "circles/3.png"
image = cv2.imread(image_path)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

# 時計の円の検出
# ハフ変換による円を検出する
circles = cv2.HoughCircles(blurred, 
                           cv2.HOUGH_GRADIENT, 
                           dp=1.5,          # 解像度の比率
                           minDist=330,     # 円の中心の最小距離、誤検出に関わる
                           param1=100,      # Cannyエッジ検出の大きい方のしきい値
                           param2=40,       # 投票数の基準
                           minRadius=800,   # 最小半径   
                           maxRadius=1400   # 最大半径
                           )

if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    x_sum = 0
    y_sum = 0
    for (x, y, r) in circles:
        x_sum += x
        y_sum += y
        # cv2.circle(image, (x, y), r, (0, 255, 0), 10)
        # cv2.circle(image, (x, y), 30, (0, 255, 0), 10)
    ave_x = x_sum // len(circles)
    ave_y = y_sum // len(circles)
    # 円の中心座標の平均をプロット
    cv2.circle(image, (ave_x, ave_y), 30, (255, 0, 0), 20)
else:
    print('円検出なし')
    exit()

# 時計の針の検出
# ハフ変換による直線の検出
edges = cv2.Canny(blurred, 20, 50, apertureSize = 3)    # Cannyエッジ検出
lines = cv2.HoughLinesP(edges,               
                        rho = 1,            
                        theta = np.pi/100,
                        threshold = 100,    
                        minLineLength = 15,   
                        maxLineGap = 100    # 検出された線を1つにまとめる
                       )

# 線分が見つかれば{x1, y1, x2, y2}のタプル、見つからなければNone
if lines is not None:
    distances = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # 線分の中心を求める
        mid_x = (x1 + x2) // 2 
        mid_y = (y1 + y2) // 2
        # 線分の中心と円の中心のユークリッド距離を求める
        # distance = np.sqrt((mid_x - x_ave) ** 2 + (mid_y - y_ave) ** 2)
        distance = np.linalg.norm(np.array([mid_x, mid_y]) - np.array([ave_x, ave_y]))
        distances.append((distance, line[0]))
    
    # 中心との距離が最も小さい２つの直線を針とする
    distances.sort()
    clock_hands = [distances[2][1], distances[1][1]]
    
    x1_1, y1_1, x1_2, y1_2 = clock_hands[0]
    x2_1, y2_1, x2_2, y2_2 = clock_hands[1]

    cv2.line(image, (x1_1, y1_1), (x1_2, y1_2), (0, 0, 255), 10)
    cv2.line(image, (x2_1, y2_1), (x2_2, y2_2), (0, 0, 255), 10)

    # 2つの直線がなす角度を計算
    angle1 = np.arctan2(y1_2 - y1_1, x1_2 - x1_1)
    angle2 = np.arctan2(y2_2 - y2_1, x2_2 - x2_1)
    # 短針は12時固定と仮定した
    # よって、それぞれの直線の角度を引いた絶対値を求めることで針の角度がわかる
    angle = np.abs(angle1 - angle2)
    time = round(np.degrees(angle)/30)
    print(np.degrees(angle))
    # 時間に変換
    # 針のなす角度は、1時間ごとに30°増加する
    print(f'{time}時')
else:
    print("直線検出なし")

# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# plt.axis('off')
# plt.show()

# 結果を保存する
cv2.imwrite('0001.png', image)

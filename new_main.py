import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = "clocks/1.png"
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
    center_ave_x = x_sum // len(circles)
    center_ave_y = y_sum // len(circles)
    # 円の中心座標の平均をプロット
    cv2.circle(image, (center_ave_x, center_ave_y), 30, (255, 0, 0), 20)
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
        line_mid_x = (x1 + x2) // 2 
        line_mid_y = (y1 + y2) // 2
        # 線分の中心と円の中心のユークリッド距離を求める
        distance = np.linalg.norm(np.array([line_mid_x, line_mid_y]) - np.array([center_ave_x, center_ave_y]))
        distances.append((distance, line[0]))
    # 円の中心との距離が近い直線が時計の針である
    # 針が12時を指すとき、長針を表す直線であり、
    # 針が12時以外を指すとき、短針を表す直線である
    # 円の中心と近い針のうち、初めて12時以外を指すものが短針であり、正しい時刻を表す
    distances.sort()

    def check_time(x1, y1, x2, y2, time):
        # 12時は除外
        if time == 0:
            return False
        # 針がx軸と平行のとき
        if y1 == y2:
            # 針が右側
            if x1 < x2:
                if time == 3:
                    return True
                else:
                    return False
            # 針が左側
            else:
                if time == 9:
                    return True
                else:
                    return False 
        # 針が上側
        if y1 > y2:
            # 12時は除外
            if x1 == x2:
                return False
            # 針が右側
            if x1 < x2:
                if 1 <= time <= 3:
                    return True
                else:
                    return False
            # 針が左側
            else:
                if 9 <= time <= 11:
                    return True
                else:
                    return False
        # 針が下側
        else:
            # 針が右側
            if x1 <= x2:
                if 4 <= time <= 6:
                    return True
                else:
                    return False
            # 針が左側
            else:
                if  7 <= time <= 9:
                    return True
                else:
                    return False
                
    for distance in distances:
        x1, y1, x2, y2 = distance[1]
        # 直線の始点を円の中心に近いものとする
        tmp1_dis = np.linalg.norm(np.array([x1, y1])-np.array([center_ave_x, center_ave_y]))
        tmp2_dis = np.linalg.norm(np.array([x2, y2])-np.array([center_ave_x, center_ave_y]))
        if tmp1_dis > tmp2_dis:
            tmp_x = x1
            x1 = x2
            x2 = tmp_x
            tmp_y = y1
            y1 = y2
            y2 = tmp_y
        
        #直線がなす角度を計算
        angle = np.arctan2(y2 - y1, x2 - x1)
        angle_degrees = np.degrees(angle)

        # 画像座標系と一般の二次元座標系の増加する方向が逆向きであるため
        # 角度の正負を入れ替える
        angle_degrees *= -1

        # 角度が負のとき、正にする
        if angle_degrees < 0:
            angle_degrees += 360

        # 12時から時計回りに角度を考える
        if 0 <= angle_degrees <= 90:
            angle_degrees = 90 - angle_degrees
        else:
            angle_degrees = 360 - angle_degrees + 90

        time = round(angle_degrees / 30)
        if (check_time(x1, y1, x2, y2, time)):
        # if time != 0:
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 10)
            print(f'{time}時')
            # 結果を保存する
            cv2.imwrite('0001.png', image)
            exit()
else:
    print("直線検出なし")
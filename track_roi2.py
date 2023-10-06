import cv2
import numpy as np
import time

# ビデオ読み込み
video_path = '../../ffmpeg/output.mov'
cap = cv2.VideoCapture(video_path)

# 初期フレームの読み込み
ret, frame = cap.read()

# ROI_1 の指定
x1, y1, w1, h1 = 1020, 450, 1313-1020, 67-455 # 例としての座標
roi_1 = (x1, y1, w1, h1)

# ROI_2 の指定 (ROI_1内で指定する)
x2, y2, w2, h2 = x1 + w1 - 50, y1, 50, int(h1/4)  # 例としての座標
roi_2 = (x2, y2, w2, h2)

# スライド速度
slide_speed = 5  # ピクセル単位でのスライド速度

# メインループ
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ROI_1描画 (緑色で描画)
    cv2.rectangle(frame, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)

    # ROI_2描画 (赤色で描画)
    cv2.rectangle(frame, (x2, y2), (x2+w2, y2+h2), (0, 0, 255), 2)

    # フレーム表示
    cv2.imshow("Frame", frame)

    # ROI_2を左に移動
    x2 -= slide_speed
    roi_2 = (x2, y2, w2, h2)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # ROI_2がROI_1から完全に出たら
    if x2 + w2 < x1:
        cv2.destroyAllWindows()
        
        # 2秒待つ
        time.sleep(2)
        
        # ROI_2を初期位置に戻す
        x2 = x1 + w1 - w2

# リソース解放
cap.release()
cv2.destroyAllWindows()

import cv2
import time

video_path = '../../ffmpeg/output.mov'
cap = cv2.VideoCapture(video_path)

# 初期フレームの読み込み
ret, frame = cap.read()

# ROI_1 の指定
x1, y1, w1, h1 = 1020, 450, 1313-1020, 667-450 # 例としての座標

# ROI_2 の初期位置指定
x2, y2, w2, h2 = x1+(w1//4)*3 , y1, (w1//4), h1

# トラッカーの初期化
tracker = cv2.TrackerCSRT_create()
tracker.init(frame, (x2, y2, w2, h2))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # ROI_1描画
    cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
    
    # トラッキングの更新
    success, roi = tracker.update(frame)
    
    # ROI_2描画
    if success:
        (x2, y2, w2, h2) = tuple(map(int, roi))
        cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        tracker.clear()
        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, (x2, y2, w2, h2))
    
    # フレーム表示
    cv2.imshow("Frame", frame)
    
    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

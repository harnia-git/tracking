import cv2
import numpy as np

# トラッキング対象を指定するための関数
def get_roi(frame):
    r = cv2.selectROI("Select", frame, False, False)
    cv2.destroyAllWindows()
    return r

# ローカルのパスから動画を読み込む
# このパスは適切に変更してください。
video_path = '../../ffmpeg/output.mov'
cap = cv2.VideoCapture(video_path)

# 初期フレームの読み込み
ret, frame = cap.read()

# トラッキング対象のROIを選択
#roi = get_roi(frame)
x_roi=1020; y_roi=450; w_roi=1313-1020; h_roi=667-455;
roi = (x_roi, y_roi, w_roi, h_roi)  # x, yはROIの左上の座標、wとhはROIの幅と高さ

# トラッカーの初期化
tracker = cv2.TrackerCSRT_create()
ret = tracker.init(frame, roi)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # トラッキングの更新
    ret, roi = tracker.update(frame)

    # ROIの座標を取得して矩形を描画
    if ret:
        p1 = (int(roi[0]), int(roi[1]))
        p2 = (int(roi[0] + roi[2]), int(roi[1] + roi[3]))
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # 結果の表示
    cv2.imshow("Tracking", frame)
    
    # 'q'キーでループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# キャプチャのリリースとウィンドウのクローズ
cap.release()
cv2.destroyAllWindows()

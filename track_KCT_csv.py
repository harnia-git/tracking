import cv2
import csv

video_path = '../../ffmpeg/output.mov'
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

x1, y1, w1, h1 = 1020, 450, 1313-1020, 667-450
init_x2, init_y2, init_w2, init_h2 = x1+(w1//4)*3, y1, w1//4, h1

tracker = cv2.TrackerKCF_create()
tracker.init(frame, (init_x2, init_y2, init_w2, init_h2))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

# 追跡対象の中心点の位置を記録するリスト
positions = []
prev_x2 = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
    success, roi = tracker.update(frame)

    if success:
        (x2, y2, w2, h2) = tuple(map(int, roi))
        cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)
        center_x2 = x2 + w2 // 2

        if prev_x2 is not None:
            # 前フレームとの水平方向の位置の差を計算
            delta_x = center_x2 - prev_x2
            positions.append(delta_x)

        prev_x2 = center_x2

        if x2 + (w2 // 3) < x1:
            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, (init_x2, init_y2, init_w2, init_h2))
            prev_x2 = None
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        tracker = cv2.TrackerKCF_create()
        tracker.init(frame, (init_x2, init_y2, init_w2, init_h2))
        prev_x2 = None

    out.write(frame)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# CSVファイルに位置の変化を書き込み
with open('positions.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Frame', 'Delta_X'])
    for i, delta in enumerate(positions):
        writer.writerow([i, delta])

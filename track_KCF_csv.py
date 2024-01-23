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

# 追跡データを記録するリスト
tracking_data = []
prev_right_x2 = None
tracker_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
    success, roi = tracker.update(frame)

    if success:
        (x2, y2, w2, h2) = tuple(map(int, roi))
        cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)
        right_x2 = x2 + w2

        delta_x = right_x2 - prev_right_x2 if prev_right_x2 is not None else 0
        tracking_data.append([x2, y2, delta_x, tracker_count])

        prev_right_x2 = right_x2

        if x2 + (w2 // 3) < x1:
            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, (init_x2, init_y2, init_w2, init_h2))
            prev_right_x2 = None
            tracker_count += 1
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        tracker = cv2.TrackerKCF_create()
        tracker.init(frame, (init_x2, init_y2, init_w2, init_h2))
        prev_right_x2 = None
        tracker_count += 1

    out.write(frame)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

# CSVファイルに追跡データを書き込み
with open('tracking_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Frame', 'ROI_X', 'ROI_Y', 'Delta_X', 'Tracker_Number'])
    for i, data in enumerate(tracking_data):
        writer.writerow([i] + data)

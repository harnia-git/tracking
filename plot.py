import matplotlib.pyplot as plt
import csv

# CSVファイルを読み込み
with open('tracking_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # ヘッダー行をスキップ

    frames = []
    delta_xs = []
    roi_xs = []
    tracker_numbers = []

    for row in reader:
        frame, roi_x, _, delta_x, tracker_number = map(int, row)
        frames.append(frame)
        delta_xs.append(delta_x)
        roi_xs.append(roi_x)
        tracker_numbers.append(tracker_number)

# 各トラッカー番号ごとにデータを集計
trackers_data = {}
for tracker_number in set(tracker_numbers):
    indices = [i for i, t in enumerate(tracker_numbers) if t == tracker_number]
    tracker_frames = [frames[i] for i in indices]
    tracker_delta_xs = [delta_xs[i] for i in indices]
    tracker_roi_xs = [roi_xs[i] for i in indices]

    integrated_delta_x = sum(tracker_delta_xs)
    roi_x_difference = tracker_roi_xs[-1] - tracker_roi_xs[0]

    trackers_data[tracker_number] = {
        'integrated_delta_x': integrated_delta_x,
        'roi_x_difference': roi_x_difference
    }

# 異なるトラッカー番号に基づいて異なる色でプロット
colors = ['blue', 'red', 'green', 'purple', 'orange']  # 5つまでのトラッカー番号を想定

plt.figure(figsize=(12, 6))

# Delta_Xのプロット
plt.subplot(1, 2, 1)
for tracker_number in trackers_data:
    indices = [i for i, t in enumerate(tracker_numbers) if t == tracker_number]
    plt.plot([frames[i] for i in indices], [delta_xs[i] for i in indices], marker='o', linestyle='-', color=colors[tracker_number], label=f'Tracker {tracker_number}')
plt.title('Delta X per Frame')
plt.xlabel('Frame')
plt.ylabel('Delta X (pixels)')
plt.legend()
plt.grid(True)

# ROI_Xのプロット
plt.subplot(1, 2, 2)
for tracker_number in trackers_data:
    indices = [i for i, t in enumerate(tracker_numbers) if t == tracker_number]
    plt.plot([frames[i] for i in indices], [roi_xs[i] for i in indices], marker='o', linestyle='-', color=colors[tracker_number], label=f'Tracker {tracker_number}')
plt.title('ROI X Position per Frame')
plt.xlabel('Frame')
plt.ylabel('ROI X Position (pixels)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show(block=False)  # 非ブロッキングモードでグラフを表示

# コンソールへの結果の出力
for tracker_number, data in trackers_data.items():
    print(f"Tracker Number: {tracker_number}")
    print(f"  Integrated Delta_X (Estimated Distance): {data['integrated_delta_x']} pixels")
    print(f"  ROI X Difference (Actual Distance): {data['roi_x_difference']} pixels")

# ユーザーの入力を待つ
input("Press Enter to continue...")

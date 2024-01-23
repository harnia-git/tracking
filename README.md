# Tracking
mylab_laptop_lx6

## track_KCF_csv02.py

このスクリプトは、オブジェクトトラッキングにKTFトラッカーを使用し、トラッキングデータをCSV形式で書き出します。

### スクリプトの概要

- トラッカー：KTC
- 出力：CSVファイル
- CSVフォーマット：`Frame, ROI_X, ROI_Y, Delta_X, Tracker_Number`

### サンプルCSVデータ

Frame,ROI_X,ROI_Y,Delta_X,Tracker_Number
0,1239,450,0,0
1,1240,451,1,0
2,1239,450,-1,0
3,1240,451,1,0
4,1239,452,-1,0
5,1240,451,1,0

このCSVデータは、各フレームでのトラッキング領域の左上角のX、Y座標（`ROI_X`, `ROI_Y`）、フレーム毎の水平方向の移動ピクセル量（`Delta_X`）、およびトラッカーの番号（`Tracker_Number`）を含んでいます。

### プロットスクリプト　plot.py


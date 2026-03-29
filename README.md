# timeline2kml

Convert Google Maps Timeline JSON exports into KML files for visualization in Google Earth or Google My Maps.

---

## Features

* Convert Google Timeline JSON → KML
* Extract visit locations and movement paths
* Provide both CLI and desktop GUI
* Works offline (no data upload)

---

## Installation

```bash
git clone https://github.com/Bikerbyte/timeline2kml.git
cd timeline2kml
pip install -r requirements.txt
```

---

## Usage

### GUI

```bash
python gui.py
```

1. Select `timeline.json`
2. Choose output `.kml`
3. Click Convert

---

### CLI

```bash
python cli.py --input timeline.json --output output.kml
```

---

### Executable (Currently Windows only.)

Download `timeline2kml.exe` from the GitHub Releases page, then run:

```
timeline2kml.exe
```

---

## Input

* Export Google Timeline on mobile phone. 
* Google Map Web don't support Timeline export anymore.

---

## Output

The generated KML file can be opened with:

* Google Earth
* Google My Maps

---

## Project Structure

```
timeline2kml/
├─ converter.py
├─ cli.py
├─ gui.py
├─ sample/
├─ requirements.txt
└─ README.md
```

---

## 中文說明

# timeline2kml
將 Google Maps Timeline 匯出的 `.json` 轉成 `.kml`，方便匯入 Google My Maps 或 Google Earth。

因網頁 Google Timeline 不再直接提供 `.kml` 匯出，此 Tool 可以協助把的旅行、通勤或生活軌跡保留下來，繪製成自己的地圖。

## 用途
- 整理旅行移動路線
- 回顧環島或自駕軌跡
- 匯入 Google My Maps 做個人地圖
- 保存自己的 Timeline 紀錄

## 使用方式
請先到 GitHub Releases 頁面下載 `timeline2kml.exe`。
1. 透過手機上輸出 Google Json 紀錄檔案
2. 請執行 timeline2kml.exe
3. 選擇 Timeline JSON
4. 選擇輸出 KML 路徑
3. 按下 `開始轉換`
5. 創建新的 MyGoogleMap (https://www.google.com/maps/d/u/0/).  
   <img width="344" height="95" alt="image" src="https://github.com/user-attachments/assets/7ba3a957-74f5-4a24-a889-066c9620cfd1" />
4. 匯入轉換後的 KML 檔案.
   <img width="251" height="239" alt="image" src="https://github.com/user-attachments/assets/236c4706-d05e-422c-87d4-22064d35f385" />
5. 完成  
   <img width="1202" height="531" alt="image" src="https://github.com/user-attachments/assets/abd2557b-efd4-453a-a999-3ab44f8cc3fa" />

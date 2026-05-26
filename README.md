# AetherLens

全離線圖片瀏覽與處理工具，支援 AI 放大、黑白上色、神經網路風格轉換 — 免 API Key、免雲端、完全離線。

## 功能

### 圖片瀏覽
- 左側目錄樹 + 縮圖網格 / 清單模式
- 單圖檢視：平移、縮放、旋轉
- 支援 PNG, JPG, BMP, GIF, WebP, PSD, TIFF

### 本機圖片處理（Pillow）
- **調整：** 亮度/對比度、色彩平衡（RGB）
- **濾鏡：** 銳利化、模糊、浮雕、邊緣偵測
- **色彩：** 轉黑白、暖色、冷色、復古（Sepia）

### AI 圖片轉換（OpenCV DNN，無需網路）
- **提升解析度** — 2x 放大 + 銳利化
- **黑白轉彩色**（Zhang et al. Caffe model）
- **風格轉換** — 9 種神經網路藝術風格：
  - 星夜（梵谷）、吶喊（孟克）、神奈川沖浪裏（葛飾北齋）
  - 糖果、繆斯、馬賽克、羽毛、烏德尼、構圖七號
- 模型初次使用自動下載，之後完全離線執行

### 列印
- **直接列印** — 縮放至一頁，置中輸出
- **分割列印** — 將大圖分割成多頁海報，可設定欄/行數、邊距、重疊，含即時預覽與單頁縮圖

### 其他
- EXIF 方向自動修正
- 刪除圖片（含確認對話框）
- 圖片屬性檢視
- 右鍵選單（縮圖模式 / 單圖模式）

## 系統需求

- Python 3.9+
- PyQt6, Pillow, opencv-python-headless, numpy

## 安裝

```bash
pip install -r requirements.txt
python main.py
```

初次使用 AI 功能時，模型檔案（約 150 MB）會自動下載至 `models/` 目錄。下載完成後所有處理完全離線執行，不再需要網路連線。

## 專案結構

```
AetherLens/
├── main.py           # 單一執行檔，含完整應用程式碼
├── models/           # 自動下載的 AI 模型（建議加入 .gitignore）
├── requirements.txt
├── LICENSE
└── README.md
```

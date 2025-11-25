# Dataset Maker - Taiwanese (閩南語) 版本使用指南

## 專案概述

Dataset Maker 是一個多用途的 TTS（Text-to-Speech）模型資料集製作工具，支援 Tortoise TTS、XTTS、StyleTTS 2、Higgs Audio、VibeVoice 和 IndexTTS 2 等模型。本指南專門針對處理 Taiwanese（閩南語）資料集的流程進行說明。

## 主要功能

- **語音轉錄**：使用 WhisperX 進行高品質語音轉錄
- **語音分割**：支援多種分割方法（靜音分割、Emilia Pipe 等）
- **資料集匯出**：支援多種格式（Base、Higgs、VibeVoice、Emilia）
- **批次處理**：支援大型資料集的批次處理
- **Gradio 介面**：提供直觀的網頁介面

## 安裝步驟

### 1. 系統需求
- Python >= 3.10
- Git
- CUDA（推薦，用於 GPU 加速）

### 2. 安裝 Astral UV
```bash
# 安裝 uv 包管理工具
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. 複製並安裝專案
```bash
git clone https://github.com/CreateIntelligens/indextts2_data_maker.git
cd indextts2_data_maker
uv sync
```

### 4. 啟動 Gradio 介面
```bash
uv run gradio_interface.py
```

介面將在 http://0.0.0.0:8860 上運行。

## Taiwanese 資料集處理流程

### 步驟 1: 準備資料
假設你的 Taiwanese 資料已經切割完成，結構如下：
```
/mnt/data/split_dataset1119/
├── train/
│   ├── drama1_001/
│   │   ├── 001/
│   │   │   ├── 001_001_000002_000001.wav
│   │   │   ├── 001_001_000002_000001.normalized.txt
│   │   │   └── ...
│   └── ...
└── test/
    └── ...
```

### 步驟 2: 轉換現有切割資料
使用 `convert_split_dataset.py` 腳本將現有資料轉換為專案兼容格式：

```bash
# 處理 train 資料集
uv run python convert_split_dataset.py --input /mnt/data/split_dataset1119/train --output /mnt/data/split_dataset_converted

# 處理 test 資料集
uv run python convert_split_dataset.py --input /mnt/data/split_dataset1119/test --output /mnt/data/split_dataset_test_converted
```

轉換後的結構：
```
split_dataset_converted/
├── wavs/          # 所有 .wav 文件
└── train.txt      # 轉錄文件，每行格式: wavs/filename.wav | transcription
```

### 步驟 3: 使用 Gradio 介面進行進一步處理

#### 3.1 建立專案
1. 在 Gradio 介面中輸入專案名稱（如 "taiwanese_dataset"）
2. 點擊 "Create Project"

#### 3.2 上傳音訊文件
1. 選擇剛建立的專案
2. 上傳 .wav 文件到 "wavs" 資料夾
3. 或者直接複製已轉換的資料到專案資料夾

#### 3.3 語音轉錄（如果需要重新轉錄）
1. 選擇語言：設定為 "zh"（中文/閩南語）
2. 選擇分割方法：建議使用 "Silence Slicer"
3. 設定參數：
   - Silence Duration: 6 秒
   - Max Segment Length: 12 秒
4. 點擊 "Transcribe" 開始處理

#### 3.4 匯出資料集
選擇適合的格式進行匯出：
- **Base 格式**：適用於 Tortoise、XTTS、StyleTTS 2、IndexTTS
- **Higgs Audio 格式**：適用於 Higgs Audio 模型
- **VibeVoice 格式**：適用於 VibeVoice 模型

## convert_to_jsonl.py 用法

`convert_to_jsonl.py` 腳本用於將 `train.txt` 格式轉換為 JSONL 格式，主要用於 IndexTTS tokenizer 訓練。

### 基本用法

```bash
uv run python convert_to_jsonl.py --input /path/to/train.txt --output /path/to/output.jsonl
```

### 參數說明
- `--input`: 輸入的 train.txt 文件路徑
- `--output`: 輸出的 JSONL 文件路徑

### 輸入格式 (train.txt)
```
wavs/filename.wav | transcription text
wavs/another.wav | another transcription
```

### 輸出格式 (JSONL)
每行一個 JSON 對象：
```json
{"id": "uuid", "text": "transcription", "audio": "/mnt/data/split_dataset_converted/wavs/filename.wav", "speaker": "speaker_id", "language": "tw"}
```

### 範例
```bash
# 將轉換後的 train.txt 轉換為 JSONL
python3 convert_to_jsonl.py --input /mnt/data/split_dataset_converted/train.txt --output /mnt/data/split_dataset_converted/train.jsonl
```

## 完整工作流程範例

### 1. 資料準備
```bash
# 轉換現有切割資料
uv run python convert_split_dataset.py --input /mnt/data/split_dataset1119/train --output /mnt/data/split_dataset_converted
uv run python convert_split_dataset.py --input /mnt/data/split_dataset1119/test --output /mnt/data/split_dataset_test_converted
```

### 2. 啟動 Gradio 介面
```bash
uv run gradio_interface.py
```

### 3. 在介面中：
- 建立專案 "taiwanese_tts"
- 上傳或複製音訊文件
- 進行轉錄（如果需要）
- 匯出為 Base 格式

### 4. 轉換為 JSONL（如果需要）
```bash
uv run python convert_to_jsonl.py \
  --input /mnt/data/split_dataset_converted/train.txt \
  --output /mnt/data/split_dataset_converted/train.jsonl
```

## 注意事項

1. **語言設定**：對於 Taiwanese 資料，建議在轉錄時設定語言為 "zh"
2. **音質**：確保音訊文件沒有背景噪音，建議先使用音訊分離工具處理
3. **分割參數**：根據音訊特點調整靜音持續時間和最大分割長度
4. **儲存空間**：處理大型資料集需要足夠的磁碟空間
5. **GPU 加速**：CUDA 可用時會自動使用 GPU 加速處理

## 故障排除

### 常見問題
1. **CUDA 錯誤**：確保 CUDA 正確安裝，參考 README 中的修復方法
2. **記憶體不足**：減少批次大小或使用 CPU 模式
3. **轉錄品質不佳**：調整分割參數或使用不同的分割方法

### 聯絡支援
如果遇到問題，請檢查：
- GitHub Issues: https://github.com/CreateIntelligens/indextts2_data_maker/issues
- 確保使用最新版本的程式碼

## 授權
本專案遵循原始授權條款。處理的資料集僅供非商業用途。
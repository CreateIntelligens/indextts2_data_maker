#!/bin/bash

# 設定錯誤時停止腳本
set -e

# === 設定區 ===
# 原始資料路徑 (Naer 資料集位置)
INPUT_DIR="/mnt/data/naer/naer"

# 輸出資料路徑 (處理後的資料存放位置)
OUTPUT_DIR="/mnt/data/naer_converted"

# ============

echo "=== 開始處理 Naer 資料集 ==="
echo "輸入目錄: $INPUT_DIR"
echo "輸出目錄: $OUTPUT_DIR"
echo "------------------------------"

# 1. 轉換資料結構
echo "[1/2] 正在執行 convert_split_dataset.py ..."
echo "      將原始資料整理至 $OUTPUT_DIR/wavs 並生成 train.txt"

uv run python convert_split_dataset.py --input "$INPUT_DIR" --output "$OUTPUT_DIR"

echo "      結構轉換完成。"

# 2. 生成 JSONL
echo "[2/2] 正在執行 convert_to_jsonl.py ..."
echo "      生成 IndexTTS 訓練用 JSONL 格式"

uv run python convert_to_jsonl.py \
    --input "$OUTPUT_DIR/train.txt" \
    --output "$OUTPUT_DIR/train.jsonl" \
    --dataset_root "$OUTPUT_DIR"

echo "------------------------------"
echo "=== 全部完成 ==="
echo "結果檔案位於:"
echo "  1. 音檔目錄: $OUTPUT_DIR/wavs"
echo "  2. 訓練清單: $OUTPUT_DIR/train.jsonl"

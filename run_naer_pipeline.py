#!/usr/bin/env python3
"""
一條龍處理腳本：將 Naer 台語語料轉換為 IndexTTS 訓練用的 JSONL 格式。

流程：
1. 呼叫 convert_split_dataset.py 將原始資料夾結構轉平，並生成 train.txt。
2. 讀取 train.txt，生成 train.jsonl，並確保路徑為絕對路徑。
"""

import argparse
import json
import uuid
import os
from pathlib import Path
from convert_split_dataset import convert_dataset

def generate_jsonl(output_root: Path):
    """
    讀取 output_root 下的 train.txt，並在同目錄生成 train.jsonl
    """
    train_txt_path = output_root / "train.txt"
    jsonl_output_path = output_root / "train.jsonl"
    
    if not train_txt_path.exists():
        print(f"錯誤: 找不到 {train_txt_path}，請檢查第一步轉換是否成功。")
        return

    print(f"正在生成 JSONL: {jsonl_output_path} ...")
    
    count = 0
    with open(train_txt_path, 'r', encoding='utf-8') as f_in, \
         open(jsonl_output_path, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            line = line.strip()
            if not line or '|' not in line:
                continue
                
            parts = line.split('|', 1)
            if len(parts) != 2:
                continue
                
            rel_wav_path = parts[0].strip() # 例如: wavs/1089_1000_xxxx.wav
            text = parts[1].strip()
            
            # 組合絕對路徑
            abs_audio_path = (output_root / rel_wav_path).resolve()
            
            # 從檔名提取 Speaker ID
            # 假設檔名格式為 1089_1000_004074_000003.wav，取第一個底線前的數字作為 Speaker
            filename = Path(rel_wav_path).name
            speaker = "unknown"
            if "_" in filename:
                speaker = filename.split('_')[0]
            
            # 建立資料物件
            record = {
                "id": str(uuid.uuid4()),
                "text": text,
                "audio": str(abs_audio_path),
                "speaker": speaker,
                "language": "tw"
            }
            
            json.dump(record, f_out, ensure_ascii=False)
            f_out.write('\n')
            count += 1

    print(f"JSONL 生成完畢。共處理 {count} 筆資料。")
    print(f"輸出檔案位置: {jsonl_output_path}")

def main():
    parser = argparse.ArgumentParser(description="Naer 資料集一條龍處理腳本")
    parser.add_argument("--input", type=str, default="/mnt/data/naer/naer", help="原始資料輸入路徑")
    parser.add_argument("--output", type=str, default="/mnt/data/naer_converted", help="轉換後資料輸出路徑")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    print(f"=== 開始執行資料處理流程 ===")
    print(f"輸入目錄: {input_path}")
    print(f"輸出目錄: {output_path}")
    
    # 步驟 1: 轉換資料結構
    print("\n[步驟 1/2] 正在轉換資料結構與複製音檔...")
    if not input_path.exists():
        print(f"錯誤: 輸入路徑不存在 {input_path}")
        return
        
    # 確保輸出目錄存在
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        convert_dataset(str(input_path), str(output_path))
    except Exception as e:
        print(f"步驟 1 發生錯誤: {e}")
        return

    # 步驟 2: 生成 JSONL
    print("\n[步驟 2/2] 正在生成 IndexTTS JSONL 格式...")
    try:
        generate_jsonl(output_path)
    except Exception as e:
        print(f"步驟 2 發生錯誤: {e}")
        return

    print("\n=== 全部完成 ===")
    print(f"您現在可以使用該 JSONL 檔案進行訓練：{output_path / 'train.jsonl'}")

if __name__ == "__main__":
    main()

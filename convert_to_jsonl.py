#!/usr/bin/env python3
"""
Convert a text file (pipe-separated: wav_path | text) to JSONL format for IndexTTS tokenizer training.
"""

import argparse
import json
import uuid
from pathlib import Path

def convert_to_jsonl(input_file: Path, output_file: Path):
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            line = line.strip()
            if line and '|' in line:
                parts = line.split('|', 1)  # Split only on first |
                if len(parts) == 2:
                    wav_path = parts[0].strip()
                    text = parts[1].strip()
                    if text:
                        # Extract speaker from wav filename (e.g., 1581_060_000083_000001.wav -> 000001_1581)
                        filename = wav_path.split('/')[-1]  # Get filename
                        name_without_ext = filename.rsplit('.', 1)[0]  # Remove .wav extension
                        parts = name_without_ext.split('_')
                        if len(parts) >= 4:
                            drama = parts[3]  # 000001
                            character = parts[0]  # 1581
                            speaker = f"{drama}_{character}"
                        else:
                            speaker = 'unknown'
                        # Convert relative path to absolute path
                        # Assuming audio files are in /mnt/data/split_dataset1119/train/
                        abs_audio_path = f"/mnt/data/split_dataset1119/train/{wav_path}"
                        record = {
                            "id": str(uuid.uuid4()),
                            "text": text,
                            "audio": f"/mnt/data/split_dataset_converted/{wav_path}",
                            "speaker": speaker,
                            "language": "tw"
                        }
                        json.dump(record, f_out, ensure_ascii=False)
                        f_out.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert pipe-separated text file to JSONL format.")
    parser.add_argument("--input", type=Path, required=True, help="Input text file (wav_path | text per line).")
    parser.add_argument("--output", type=Path, required=True, help="Output JSONL file.")
    args = parser.parse_args()
    
    convert_to_jsonl(args.input, args.output)
    print(f"Converted {args.input} to {args.output}")
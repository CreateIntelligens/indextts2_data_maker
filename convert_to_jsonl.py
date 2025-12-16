#!/usr/bin/env python3
"""
Convert a text file (pipe-separated: wav_path | text) to JSONL format for IndexTTS tokenizer training.
"""

import argparse
import json
import uuid
from pathlib import Path

def convert_to_jsonl(input_file: Path, output_file: Path, dataset_root: Path = None):
    """
    Args:
        input_file: Path to train.txt
        output_file: Path to output .jsonl
        dataset_root: Root directory of the converted dataset (containing wavs/ folder). 
                      Used to generate absolute paths.
    """
    
    print(f"Converting {input_file} -> {output_file}")
    if dataset_root:
        print(f"Using dataset root for absolute paths: {dataset_root}")

    count = 0
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            line = line.strip()
            if not line or '|' not in line:
                continue
                
            parts = line.split('|', 1)
            if len(parts) == 2:
                rel_wav_path = parts[0].strip() # e.g., wavs/filename.wav
                text = parts[1].strip()
                
                if not text:
                    continue

                # Determine absolute audio path
                if dataset_root:
                    # Resolve absolute path
                    abs_audio_path = (dataset_root / rel_wav_path).resolve()
                else:
                    # Fallback if no root provided (though usually required for training)
                    abs_audio_path = Path(rel_wav_path).resolve()

                # Extract speaker from filename
                # Strategy: Use the first part of the filename separated by '_'
                # e.g., 1089_1000_004074_000003.wav -> speaker: 1089
                filename = Path(rel_wav_path).name
                if '_' in filename:
                    speaker = filename.split('_')[0]
                else:
                    speaker = 'unknown'

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
    
    print(f"Done. Processed {count} lines.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert pipe-separated text file to JSONL format.")
    parser.add_argument("--input", type=Path, required=True, help="Input text file (wav_path | text per line).")
    parser.add_argument("--output", type=Path, required=True, help="Output JSONL file.")
    parser.add_argument("--dataset_root", type=Path, default=None, help="Root directory of the dataset to construct absolute paths.")
    
    args = parser.parse_args()
    
    convert_to_jsonl(args.input, args.output, args.dataset_root)

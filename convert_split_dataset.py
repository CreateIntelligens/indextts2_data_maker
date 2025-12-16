#!/usr/bin/env python3
"""
Script to convert the existing split dataset structure to the dataset-maker format.
This script assumes the structure described by the user:
- /mnt/data/split_dataset1119/train/ contains subfolders like drama1_001, etc.
- Each subfolder has numeric subfolders (e.g., 001, 014) containing .wav and .normalized.txt files.
- .normalized.txt contains the transcription for the corresponding .wav file.

Output: A new folder with 'wavs/' subfolder and 'train.txt' file in the format:
wavs/filename.wav | transcription
"""

import os
import shutil
from pathlib import Path

def convert_dataset(input_root: str, output_root: str):
    """
    Convert the dataset from the user's structure to dataset-maker format.

    Args:
        input_root: Path to /mnt/data/split_dataset1119/train/
        output_root: Path to the output dataset folder (e.g., /home/ubuntu/dataset-maker/datasets_folder/my_dataset)
    """
    input_path = Path(input_root)
    output_path = Path(output_root)
    wavs_dir = output_path / "wavs"
    wavs_dir.mkdir(parents=True, exist_ok=True)

    train_txt_path = output_path / "train.txt"

    entries = []

    # Traverse all files recursively
    for file in input_path.rglob('*.wav'):
        if not file.is_file():
            continue
            
        # Find corresponding .normalized.txt
        txt_file = file.with_suffix('.normalized.txt')
        if not txt_file.exists():
            # Try checking if there's a txt file with the same name but excluding extension logic might vary
            # But per user description, it's .normalized.txt
            print(f"Warning: No transcription file for {file}")
            continue

        # Read transcription
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                transcription = f.read().strip()
        except Exception as e:
            print(f"Error reading {txt_file}: {e}")
            continue

        # Copy wav file to wavs/ with a simple name
        # Use the original filename but ensure uniqueness
        new_wav_name = file.name
        new_wav_path = wavs_dir / new_wav_name

        # Handle potential name conflicts
        counter = 1
        while new_wav_path.exists():
            stem = file.stem
            suffix = file.suffix
            new_wav_name = f"{stem}_{counter}{suffix}"
            new_wav_path = wavs_dir / new_wav_name
            counter += 1

        shutil.copy2(file, new_wav_path)

        # Add entry
        relative_path = f"wavs/{new_wav_name}"
        entries.append(f"{relative_path} | {transcription}")

        if len(entries) % 100 == 0:
            print(f"Processed {len(entries)} files...", end='\r')
    
    print() # Newline after progress

    # Write train.txt
    with open(train_txt_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(entry + '\n')

    print(f"Conversion complete. {len(entries)} entries written to {train_txt_path}")
    print(f"Audio files copied to {wavs_dir}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert split dataset to dataset-maker format.")
    parser.add_argument("--input", required=True, help="Path to input folder (e.g., /mnt/data/split_dataset1119/train)")
    parser.add_argument("--output", required=True, help="Path to output folder (e.g., /home/ubuntu/dataset-maker/datasets_folder/split_dataset_converted)")

    args = parser.parse_args()

    convert_dataset(args.input, args.output)
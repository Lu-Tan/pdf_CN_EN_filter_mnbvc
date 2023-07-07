import json
import shutil
import os

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--src_path",
        type=str,
        help="The jsonl path with PDF paths in each line.",
    )   
    parser.add_argument(
        "--tgt_folder",
        type=str,
        help="The target directory for copied PDF files.",
    )
    parsed_args = parser.parse_args()
    return parsed_args

args = parse_arguments()

src_path = args.src_path
tgt_foler = args.tgt_folder
if not os.path.exists(tgt_foler):
    os.makedirs(tgt_foler)

with open(src_path, 'r') as file:
    lines = file.readlines()
for line in lines:
    file_path = line.strip()[1:-1] 
    shutil.copy(file_path, tgt_foler)
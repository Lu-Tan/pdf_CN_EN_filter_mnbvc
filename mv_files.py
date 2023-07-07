import json
import shutil
import os

src_path = '/Users/tanlu/Documents/PDF_classifier/pdf2txt_mnbvc-master/pdf_cls_results/CN_pdf_file.jsonl'
tgt_foler = 'CN_PDF'
if not os.path.exists(tgt_foler):
    os.makedirs(tgt_foler)

with open(src_path, 'r') as file:
    lines = file.readlines()
for line in lines:
    file_path = line.strip()[1:-1] 
    shutil.copy(file_path, tgt_foler)
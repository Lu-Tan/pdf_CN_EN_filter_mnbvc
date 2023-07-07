#!/usr/bin/env python3
# -*- coding:utf8 -*-
"""
 Author: Lu Tan
 Create Time: 2023/7/7
"""
import pdf_lan_filter
import os 

pdf_directory = '../pdf/2023'
pdf_cls_results = 'pdf_cls_results'
if not os.path.exists(pdf_cls_results):
    os.makedirs(pdf_cls_results)

text_only_list = []
more_than_text_list = []
CN_pdf_list = []
EN_pdf_list = []
CN_EN_pdf_list = []
other_lan_pdf_list = []

# go through all PDF files
for root, dir, files in os.walk(pdf_directory):
    for file in files:
        if file.endswith('.pdf'):
            src_file = os.path.join(root, file)
            pdf_lan_filter.check_pdf_cls(src_file, text_only_list, more_than_text_list, CN_pdf_list, EN_pdf_list, CN_EN_pdf_list, other_lan_pdf_list)
    
# save results
text_only_file = os.path.join(pdf_cls_results, 'txt_only_file.jsonl')
pdf_lan_filter.save_list2jsonl(text_only_list, text_only_file)
print("There are " + str(len(text_only_list)) + ' PDF files contains text ONLY.')

more_than_text_file = os.path.join(pdf_cls_results, 'more_than_txt_file.jsonl')
pdf_lan_filter.save_list2jsonl(more_than_text_list, more_than_text_file)
print("There are " + str(len(more_than_text_list) + ' PDF files contains more than text.(image, tables, etc.)'))

CN_pdf_file = os.path.join(pdf_cls_results, 'CN_pdf_file.jsonl')
pdf_lan_filter.save_list2jsonl(CN_pdf_list, CN_pdf_file)
print("There are " + str(len(CN_pdf_list)) + ' PDF files contains Chinese text ONLY.')

EN_pdf_file = os.path.join(pdf_cls_results, 'EN_pdf_file.jsonl')
pdf_lan_filter.save_list2jsonl(EN_pdf_list, EN_pdf_file)
print("There are " + str(len(EN_pdf_list)) + ' PDF files contains English text ONLY.')

CN_EN_pdf_file = os.path.join(pdf_cls_results, 'CN_EN_pdf_file.jsonl')
pdf_lan_filter.save_list2jsonl(CN_EN_pdf_list, CN_EN_pdf_file)
print("There are " + str(len(CN_EN_pdf_list)) + ' PDF files contains Chinese and English text ONLY.')


other_lan_pdf_file = os.path.join(pdf_cls_results, 'other_lan_pdf_file.jsonl')
pdf_lan_filter.save_list2jsonl(other_lan_pdf_list, other_lan_pdf_file)
print("There are " + str(len(other_lan_pdf_list)) + ' PDF files contains other languages, more than Chinese and English.')



#!/usr/bin/env python3
# -*- coding:utf8 -*-
import os 
import argparse
from loguru import logger 
from tqdm import tqdm
import json
from datetime import datetime
import pdfplumber
from lingua import Language, LanguageDetectorBuilder
import re
import string
from zhon.hanzi import punctuation

def parse_arguments():
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pdf_directory",
        type=str,
        default='./pdfs',
        required=True,
        help="The directory containing the PDF files to be classified.",
    )   
    parser.add_argument(
        "--log_directory",
        type=str,
        default='./log',
        help="The directory where the log files will be saved.",
    )
    parser.add_argument(
        '--identify_elements',
        type=int,
        default = 1,
        help='Identify what elements are contained in this page. Ex: image, text, form.'
    )
    parser.add_argument(
        '--identify_languages',
        type=int,
        default=1,
        help='Identify the languages of this page.'
    )
    return parser.parse_args()

def remove_symbols(text):
    # 移除文本中的符号
    symbols = string.punctuation + '\\n\\t\\r' + '-'  
    translator = str.maketrans('', '', symbols)
    text_without_symbols = text.translate(translator)
    return text_without_symbols

def remove_CN_symbols(text):
    # 移除文本中的中文符号
    if text in punctuation:
        return ''
    else:
        return text

def identify_pdf_elements(page):
    obj_type = set()
    # ---contain text only---
    if len(page.images) > 0:  # 页面包含图像
        # print("There are " + str(len(page.images)) + ' images in page ' + str(page.page_number) + ' in file ' + src_file)
        obj_type.add('image')
    if len(page.lines) > 0:  # 页面包含表单
        # print('There might be some tables in page ' + str(page.page_number) + ' in file ' + src_file)
        obj_type.add('form')
    if len(page.chars) > 0:  # 页面包含文本
        # print('There are texts in page ' + str(page.page_number) + ' in file ' + src_file)
        obj_type.add('text')
    if 'text' in obj_type and len(obj_type) == 1:
        text_only = 1
    else:
        text_only = 0
    return {
        "page_number": int(page.page_number), 
        "obj_type":list(obj_type),
        "text_only": text_only, 
        }

def identify_languages(page):
    languages = [Language.ENGLISH, Language.CHINESE]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()

    unidentified_chars = set()
    LAN_res = set()
    chars = page.chars # a list of dicts
    for c in tqdm(chars, desc='processing page ' + str(page.page_number)):
        _c = c['text']
        _c = _c.strip()
        _c = re.sub(r'[0-9]+', '', _c)
        _c = remove_symbols(_c)
        _c = remove_CN_symbols(_c)
        if _c:
            LAN = detector.detect_language_of(_c)
            if LAN == None:
                unidentified_chars.add(c['text'])
            LAN_res.add(str(LAN))
    return LAN_res, unidentified_chars 


def classify_pdf_files(pdf_directory):
    # 分类PDF文件
    pdf_info = []
    for root, _, files in tqdm(os.walk(pdf_directory), desc="Processing PDF files"):
        for file in files:
            if file.endswith('.pdf'):
                try:
                    src_file = os.path.join(root, file)
                    pages = []
                    with pdfplumber.open(src_file) as pdf:
                        for page in pdf.pages:
                            pdf_elements = identify_pdf_elements(page)
                            pdf_elements['file_path'] =  src_file
                            if pdf_elements['text_only']:
                                pdf_language, unidentified_chars = identify_languages(page)
                                pdf_elements['language_type'] = list(pdf_language)
                                pdf_elements['unidentified_chars'] = list(unidentified_chars)
                            pdf_info.append(pdf_elements)
                except Exception as e:
                    logger.error(f"Error while processing file {file}: {e}") 
    return pdf_info

def save_results(pdf_info, output_file):
    # 保存分类结果
    with open(output_file, 'w', encoding='utf-8') as file:
        for item in pdf_info:
            json.dump(item, file)
            file.write('\n')

def main():
    # 主函数
    args = parse_arguments()
    
    # 获取时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 配置logger
    logger.add(f"{args.log_directory}/pdf_classifier_{timestamp}.log", rotation="500 MB") 

    pdf_info = classify_pdf_files(args.pdf_directory)

    save_results(pdf_info, 'pdf_classification.jsonl')

    logger.info("PDF classification completed.") 

if __name__ == "__main__":
    main()

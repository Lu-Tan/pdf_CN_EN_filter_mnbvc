#!/usr/bin/env python3
# -*- coding:utf8 -*-
import utils
import os 
import argparse
from loguru import logger
from tqdm import tqdm
import json
from datetime import datetime

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
    return parser.parse_args()

def classify_pdf_files(pdf_directory):
    # 分类PDF文件
    pdf_info = []
    for root, _, files in tqdm(os.walk(pdf_directory), desc="Processing PDF files"):
        for file in files:
            if file.endswith('.pdf'):
                src_file = os.path.join(root, file)
                try:
                    checker = utils.PDFChecker(src_file)
                    pdf_class = checker.check_pdf_cls()
                    pdf_info.append({"file_path": src_file, "class": pdf_class})
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

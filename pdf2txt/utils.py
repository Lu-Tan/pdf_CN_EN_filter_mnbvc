#!/usr/bin/env python3
# -*- coding:utf8 -*-
"""
 Author: Lu Tan
 Create Time: 2023/7/1
"""
# from langchain.document_loaders import PyPDFLoader, PyMuPDFLoader, PDFMinerLoader
from typing import List, Optional

import numpy as np
import fitz
import re
import string


from .layout import page_layout


def check_text_only(src_file: str):
    print(f"start checking {src_file}." )
    doc = fitz.open(src_file, filetype='pdf')
    assert isinstance(doc, fitz.Document)
    for page in doc:
        assert isinstance(page, fitz.Page)
        if not check_page_format(page):
            print(src_file + ' is not qualified.')
            return False
    return True


def check_for_tables(page):
    tables_found = False
    text = page.get_text()
    if "+" in text:
        tables_found = True # found tables
    return tables_found # found no tables 


def check_page_format(page: fitz.Page):
    # check if there's a figure or not
    image_list = page.get_images()
    if len(image_list) > 0: 
        print("Found " + str(len(image_list)) + " image in page " + str(page.number))
        return False 
    elif page.first_widget: # check if there's a form or not
        print("Found form in page " + str(page.number))
    elif check_for_tables(page): # check if there's a table or not
        print("Found table in page + " + str(page.number))
        # todo: add more option formats that is not text
    else:
        return True 


def remove_symbols(text):
    symbols = string.punctuation + '\n\t\r' + '-'  # 英文标点符号， 换行符、制表符
    translator = str.maketrans('', '', symbols)
    text_without_symbols = text.translate(translator)

    return text_without_symbols

def remove_CN_symbles(text):
    # 定义正则表达式模式匹配全角半角标点符号
    pattern = r'[^\w\s]'
    text_without_punctuation = re.sub(pattern, '', text)
    return text_without_punctuation
    

def check_text_contains_only_english_and_numbers(file_path):
    english_and_numbers_only = True
    with fitz.open(file_path) as doc:
        for page in doc:
            text = page.get_text()
            text = remove_symbols(page.get_text())
            text = remove_CN_symbles(text)
            pattern = re.compile(r'[^a-zA-Z0-9\s]+')
            if pattern.search(text):
                print(pattern.search(text))
                english_and_numbers_only = False
                break
    return english_and_numbers_only

def check_text_contains_only_chinese_and_numbers(file_path):
    chinese_and_numbers_only = True
    pattern = re.compile(r'[^\u4e00-\u9fa50-9\s]+')

    with fitz.open(file_path) as doc:
        for page in doc:
            text = remove_symbols(page.get_text())
            text = remove_CN_symbles(text)
            if pattern.search(text):
                chinese_and_numbers_only = False
                break
    return chinese_and_numbers_only

def check_text_contains_only_CN_EN_and_numbers(file_path):
    CN_EN_and_numbers_only = True
    pattern = re.compile(r'[^\u4e00-\u9fa50-9a-zA-Z\s]+')

    with fitz.open(file_path) as doc:
        for page in doc:
            text = remove_symbols(page.get_text())
            text = remove_CN_symbles(text)
            if pattern.search(text):
                CN_EN_and_numbers_only = False
                break
    return CN_EN_and_numbers_only



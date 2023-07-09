#!/usr/bin/env python3
# -*- coding:utf8 -*-
"""
Author: Lu Tan
Create Time: 2023/7/1
"""
import fitz
import re
import string
import json

class PDFChecker:
    def __init__(self, src_file):
        self.src_file = src_file
        self.pages = []
        self.load_pages()  # 在初始化时加载PDF的所有页面

    def load_pages(self):
        # 尝试打开PDF文件并加载所有页面
        try:
            with fitz.open(self.src_file, filetype='pdf') as doc:
                self.pages = [page for page in doc]
        except Exception as e:
            print(f"Error loading pages from {self.src_file}: {e}")

    def check_page_format(self, page):
        # 检查页面格式，如果页面包含图像、表单或表格，则返回False
        image_list = page.get_images()
        if len(image_list) > 0:  # 页面包含图像
            return False 
        elif page.first_widget:  # 页面包含表单
            return False
        elif self.check_for_tables(page):  # 页面包含表格
            return False
        else:  # 页面只包含文本
            return True 

    def check_for_tables(self, page):
        # 检查页面是否包含表格，如果包含，则返回True
        tables_found = False
        text = page.get_text()
        if "+" in text:
            tables_found = True
        return tables_found

    def check_text_only(self):
        # 检查PDF是否只包含文本，如果包含非文本元素，则返回False
        for page in self.pages:
            if not self.check_page_format(page):
                return False
        return True

    def remove_symbols(self, text):
        # 移除文本中的符号
        symbols = string.punctuation + '\\n\\t\\r' + '-'  
        translator = str.maketrans('', '', symbols)
        text_without_symbols = text.translate(translator)
        return text_without_symbols

    def remove_CN_symbles(self, text):
        # 移除文本中的中文符号
        pattern = r'[^\\w\\s]'
        text_without_punctuation = re.sub(pattern, '', text)
        return text_without_punctuation

    def check_text_contains_only_specified_characters(self, pattern):
        # 检查文本是否只包含指定的字符
        specified_characters_only = True
        for page in self.pages:
            text = page.get_text()
            text = self.remove_symbols(text)
            text = self.remove_CN_symbles(text)
            if pattern.search(text):
                specified_characters_only = False
                break
        return specified_characters_only

    def check_pdf_content(self):
        # 检查PDF的内容类型，如果只包含文本，则返回'text_only'，否则返回'more_than_text'
        if self.check_text_only():
            return 'text_only'
        else:
            return 'more_than_text'

    def check_text_language(self):
        # 检查文本的语言类型，如果只包含中文和数字，则返回'CN'，如果只包含英文和数字，则返回'EN'，如果包含中文、英文和数字，则返回'CN_EN'，否则返回'other'
        if self.check_text_contains_only_specified_characters(re.compile(r'[^\\u4e00-\\u9fa50-9\\s]+')):
            return 'CN'
        elif self.check_text_contains_only_specified_characters(re.compile(r'[^a-zA-Z0-9\\s]+')):
            return 'EN'
        elif self.check_text_contains_only_specified_characters(re.compile(r'[^\\u4e00-\\u9fa50-9a-zA-Z\\s]+')):
            return 'CN_EN'
        else:
            return 'other'

    def check_pdf_cls(self):
        # 检查PDF的内容类型和语言类型
        content_type = self.check_pdf_content()
        if content_type == 'text_only':
            language_type = self.check_text_language()
        else:
            language_type = 'more_than_text'
        return {'content_type': content_type, 'language_type': language_type}

# def save_list2jsonl(res_list, jsonl_file):
#     # 将结果列表保存为jsonl文件
#     with open(jsonl_file, 'w') as file:
#         for item in res_list:
#             json.dump(item, file)
#             file.write('\\n')

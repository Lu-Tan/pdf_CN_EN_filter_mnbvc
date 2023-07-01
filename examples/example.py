#!/usr/bin/env python3
# -*- coding:utf8 -*-
"""
 Create Time: 2023/7/1
"""
import pdf2txt

# src_file = '/Users/tanlu/Documents/PDF classifier/pdf/2023/demo/pdf/CN_test.pdf'
src_file = '/Users/tanlu/Documents/PDF classifier/pdf/2023/download/libgen/13000/1ce399e98134851b33de6a1c0e750be0.pdf'

if pdf2txt.check_text_only(src_file):
    print(src_file + ' contains TEXT only.')
    if pdf2txt.check_text_contains_only_chinese_and_numbers(src_file):
        print(src_file + ' is made up of Chinese words and numbers')
    elif pdf2txt.check_text_contains_only_english_and_numbers(src_file):
        print(src_file + ' is made up of English words and numbers')
    elif pdf2txt.check_text_contains_only_CN_EN_and_numbers(src_file):
        print(src_file + ' is made up of Chinses words, English words and numbers')
    else:
        print(src_file + ' is more than Chinese words, English words and numbers')
else:
    print(src_file + ' is composed of more than texts.')



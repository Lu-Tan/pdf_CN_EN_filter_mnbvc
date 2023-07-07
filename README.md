[TOC]

## Intro
找到只包含中文，或者只包含英文和数字的PDF。若包含图片、表格以及其他语言则丢弃。

## Usage
在 example.py中，通过 pdf_directory 参数指定待分类的PDF目录； 通过 pdf_cls_results 指定存储分类结构的 jsonl 文件的目录。即可对PDF分类，并把分类结构存储起来。
```
export PYTHONPATH="$PYTHONPATH:$PWD"

python examples/example.py --pdf_directory '../pdf/2023' --pdf_cls_results 'pdf_cls_results' > logging.log 2>&1
```

examples/example.py 将把所有PDF的名称放入到 pdf_cls_results 目录（不存在则新建）下的多个 jsonl 文件中。
做完分类得到多个 jsonl 文件后，可运行 mv_files.py 把某个 jsonl 文件中的 PDF 文件复制到指定目录。
```
python mv_files.py --src_path '/Users/tanlu/Documents/PDF_classifier/pdf2txt_mnbvc-master/pdf_cls_results/CN_pdf_file.jsonl' --tgt_folder 'CN_PDF'
```

## Features
- [x] 检查是否有图像、表格，有则报错
- [x] 用正则表达式找出只包含中文、英文、中文和英文的PDF。
  - [x] 不少英文PDF包含法语字母, 这部分PDF也分类到“非英文”。


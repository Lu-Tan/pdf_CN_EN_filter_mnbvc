# PDF 分类器 

- 目前只支持中英文

该项目是 MNBVC 计划的一部分，旨在提供一些用于对 PDF 文件进行分类和复制的工具。可以根据 PDF 文件中的文本内容来判断其是否只包含中文，或者是否包含英文和数字。若文件中包含图片、表格或其他语言，则会将其丢弃。

## 使用方法

### PDF 复制和重命名

在 `script.py` 中，通过命令行参数指定源文件夹路径、目标文件夹路径以及其他可选参数。运行脚本即可将 PDF 文件复制到目标文件夹并按顺序重命名。

```shell
python script.py --source_folder 源文件夹的路径 --destination_folder 目标文件夹的路径 --jsonline_folder ./log --encoding utf-8
```

- `--source_folder`：指定源文件夹的路径。
- `--destination_folder`：指定目标文件夹的路径。
- `--jsonline_folder`（可选）：指定保存 JSON 文件的路径，默认为 `./log`。
- `--encoding`（可选）：指定 JSON 文件的编码类型，默认为 `utf-8`。

### PDF 分类

在 `pdf_lang_classifier.py` 中，通过命令行参数指定待分类的 PDF 文件所在的目录。运行脚本即可对 PDF 进行分类，并将分类结果保存到 `pdf_classification.jsonl` 文件中。

```shell
python pdf_lang_classifier.py --pdf_directory PDF文件所在目录 --log_directory 日志文件保存目录
```

- `--pdf_directory`：指定待分类的 PDF 文件所在的目录。
- `--log_directory`（可选）：指定日志文件的保存目录，默认为 ./log。

### 复制分类结果

在完成分类并得到多个 JSONL 文件后，可以运行 `copy_files.py` 脚本将某个 JSONL 文件中的 PDF 文件复制到指定目录。

```shell
python mv_files.py --src_path '/Users/tanlu/Documents/PDF_classifier/pdf2txt_mnbvc-master/pdf_cls_results/CN_pdf_file.jsonl' --tgt_folder 'CN_PDF'
```

以上命令将复制指定 JSONL 文件中的 PDF 文件到 `CN_PDF` 目录中。

## 功能特点

- [x] 自动创建目标文件夹，如果目标文件夹已存在，则将新的 PDF 文件添加到其中。
- [x] 当源文件夹中的文件数量超过 1 万个时，脚本会自动创建子文件夹并按每个子文件夹存放的最大数量进行分组。
- [x] 生成 JSON 文件记录每个文件的原始路径和新路径，方便后续查阅和管理。
- [x] 检查 PDF 文件中的文本内容，根据中文和英文数字的比例进行分类。
- [x]  自动处理指定目录下的所有 PDF 文件，并生成分类结果。

## MNBVC 计划

本项目是 MNBVC 计划的一部分。更多关于 MNBVC 计划的信息，请访问 [MNBVC GitHub 页面](https://github.com/esbatmop/MNBVC)。


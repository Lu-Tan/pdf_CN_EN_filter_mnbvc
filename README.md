# PDF 分类器 

- 目前只支持中英文

该项目是 MNBVC 计划的一部分，旨在提供一些用于对 PDF 文件进行分类和复制的工具。可以根据 PDF 文件中的文本内容来判断其是否只包含中文，或者是否包含英文和数字。若文件中包含图片、表格或其他语言，则会将其丢弃。

## 使用方法

### PDF 复制和重命名

在 `script.py` 中，通过命令行参数指定源文件夹路径、目标文件夹路径以及其他可选参数。运行脚本即可将 PDF 文件复制到目标文件夹并按顺序重命名。

```shell
python script.py --source_folder 源文件夹的路径 --destination_folder 目标文件夹的路径 --jsonline_folder ./log --encoding utf-8
```

<!-- python pdf_copy_rename.py --source_folder /Users/tanlu/Documents/PDF_classifier/pdf --destination_folder /Users/tanlu/Documents/PDF_classifier/renamed_pdf --jsonline_folder ./log --encoding utf-8 -->

- `--source_folder`：指定源文件夹的路径。
- `--destination_folder`：指定目标文件夹的路径。
- `--jsonline_folder`（可选）：指定保存 JSON 文件的路径，默认为 `./log`。
- `--encoding`（可选）：指定 JSON 文件的编码类型，默认为 `utf-8`。

### PDF 分类

在 `pdf_lang_classifier.py` 中，通过命令行参数指定待分类的 PDF 文件所在的目录。运行脚本即可对 PDF 进行分类，并将分类结果保存到 `pdf_classification.jsonl` 文件中。

```shell
python pdf_lang_classifier.py --pdf_directory PDF文件所在目录 --log_directory 日志文件保存目录
```
<!-- 全中文的测试：
python pdf_lang_classifier.py --pdf_directory /Users/tanlu/Documents/PDF_classifier/test_pdf/test 
其他测试：
python pdf_lang_classifier.py --pdf_directory /Users/tanlu/Documents/PDF_classifier/test_pdf/0001 -->

- `--pdf_directory`：指定待分类的 PDF 文件所在的目录。
- `--log_directory`（可选）：指定日志文件的保存目录，默认为 ./log。

#### 分类结果说明
- 分类结果 jsonl 文件包含很多行，每一行代表某个PDF文件的某一页。
- 只对 "obj_type" 为 "text" 的页面做语言类别分析
- "language_type"是一个 list, 若包含 "None"，则说明此页面包含了除中英文以外的字符。
  

### 检测PDF内是否只包含文字
在 `pdf_lang_classifier.py` 中，通过修改 `--identify_languages` 参数为0，然后指定待分类的 PDF 文件所在的目录，运行脚本即可对 PDF 进行分类，并将分类结果保存到 `pdf_classification.jsonl` 文件中。

```shell
python pdf_lang_classifier.py --pdf_directory PDF文件所在目录 --log_directory 日志文件保存目录 --identify_languages 0
```

- `--pdf_directory`：指定待分类的 PDF 文件所在的目录。
- `--log_directory`（可选）：指定日志文件的保存目录，默认为 ./log。
- `--identify_languages`: 是否识别文字的语言类型。默认为1，但若只需检测 PDF 是否只包含文字而无需检测文字的语言类型时，建议指定为0.

<!-- python pdf_lang_classifier.py --pdf_directory /Users/tanlu/Documents/PDF_classifier/test_pdf/test --identify_languages 0 -->

#### 分类结果说明
- 分类结果 jsonl 文件包含很多行，每一行代表某个PDF文件的某一页的结果。
- 若 "text_only" 为1，则说明该页 PDF 只包含文本，不包含图片以及可能存在的表格。
  


### 复制分类结果

在完成分类并得到多个 JSONL 文件后，可以运行 `copy_files.py` 脚本将某个 JSONL 文件中的 PDF 文件复制到指定目录。

```shell
python copy_files.py --src_path '/Users/tanlu/Documents/PDF_classifier/pdf_CN_EN_filter_mnbvc/pdf_classification.jsonl' --tgt_folder 'CN_PDF'
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


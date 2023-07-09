import os
import shutil
import jsonlines
from tqdm import tqdm
import argparse

def copy_and_rename_pdfs(source_folder, destination_folder, jsonline_folder="./log", encoding='utf-8'):
    # 创建目标文件夹
    os.makedirs(destination_folder, exist_ok=True)

    # 初始化计数器和子文件夹编号
    count = 0
    subfolder_num = 0

    # 创建jsonline记录文件，并指定编码类型
    jsonline_file = os.path.join(jsonline_folder, 'pdf_rename_records.jsonl')
    with open(jsonline_file, mode='w', encoding=encoding) as file:
        writer = jsonlines.Writer(file)

        # 获取源文件夹下所有文件的总数
        total_files = sum(len(files) for _, _, files in os.walk(source_folder))

        # 遍历源文件夹中的所有文件和子文件夹，并使用tqdm进行监控
        for root, dirs, files in tqdm(os.walk(source_folder), total=total_files, ncols=100, desc='复制进度'):
            for file in files:
                # 检查文件扩展名是否为PDF
                if file.lower().endswith('.pdf'):
                    count += 1

                    # 超过1万个文件时，创建新的子文件夹
                    if count % 10000 == 1:
                        subfolder_num += 1
                        subfolder_name = str(subfolder_num).zfill(4)
                        os.makedirs(os.path.join(destination_folder, subfolder_name), exist_ok=True)

                    # 构建原文件的完整路径和新文件的路径
                    source_path = os.path.join(root, file)
                    new_filename = f"{count:04}.pdf"
                    destination_path = os.path.join(destination_folder, subfolder_name, new_filename)

                    # 复制文件并记录路径信息到jsonline文件
                    shutil.copy(source_path, destination_path)
                    writer.write({'original_path': source_path, 'output_path': destination_path})

    print("文件复制和重命名完成。")
    print("JSON文件保存在:", jsonline_file)

def main():
    parser = argparse.ArgumentParser(description='复制和重命名PDF文件')
    parser.add_argument('--source_folder', type=str, help='源文件夹的路径', required=True)
    parser.add_argument('--destination_folder', type=str, help='目标文件夹的路径', required=True)
    parser.add_argument('--jsonline_folder', type=str, default='./log', help='JSON文件保存路径，默认为"./log"')
    parser.add_argument('--encoding', type=str, default='utf-8', help='JSON文件编码类型，默认为"utf-8"')
    args = parser.parse_args()

    source_folder = args.source_folder
    destination_folder = args.destination_folder
    jsonline_folder = args.jsonline_folder
    encoding = args.encoding

    copy_and_rename_pdfs(source_folder, destination_folder, jsonline_folder, encoding)

if __name__ == '__main__':
    main()

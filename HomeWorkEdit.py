import argparse
import pandas as pd
import os
import re
import shutil
from pathlib import Path
from HomeWorkEdition import read_txt_file


def find_missing_students(name_id_dict, submitted_students):
    all_students = set(name_id_dict.keys())
    submitted_set = set(submitted_students)
    missing_students = all_students - submitted_set

    return [(name_id_dict[name], name) for name in missing_students]


def process_homework(source_folder, destination_folder, course_name, name_id_dict, class_name):
    try:
        # 确保目标文件夹存在
        os.makedirs(destination_folder, exist_ok=True)
        submitted_students = []  # 存储已经提交作业的学生

        # 遍历源文件夹中的文件
        for filename in os.listdir(source_folder):
            source_filepath = os.path.join(source_folder, filename)
            # 使用正则表达式匹配文件名中的学生姓名
            for name in name_id_dict:
                # 如果提供了课程名，则在正则表达式中包含它
                if course_name:
                    pattern = re.compile(f"{name}.*{course_name}", re.IGNORECASE)
                else:
                    pattern = re.compile(f"{name}", re.IGNORECASE)

                if pattern.search(filename):
                    submitted_students.append(name) # 提交的学生名单
                    # 文件的后缀
                    suffix = Path(filename).suffix
                    # 构建目标文件路径
                    destination_filepath = os.path.join(destination_folder, f"{class_name}{str(name_id_dict[name])[-CONFIG['student_num']:]}{name}{suffix}")

                    # 将文件移动/复制到目标文件夹
                    if CONFIG['move']:
                        shutil.move(source_filepath, destination_filepath)
                    else:
                        shutil.copy(source_filepath, destination_filepath)

        missing_students = find_missing_students(name_id_dict, submitted_students)
        for student_id, name in missing_students:
            print(f"学号: {student_id}\n姓名: {name}\n")

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process homework files.')
    parser.add_argument('--class_name', type=str, required=True, help='The class name')
    parser.add_argument('--student_list', type=str, required=True, help='Path to the student list file')
    parser.add_argument('--folder_path', type=str, required=True, help='Path to the source folder')
    parser.add_argument('--target_folder_path', type=str, required=True, help='Path to the target folder')
    parser.add_argument('--student_num', type=int, required=True, help='The number of digits in the student ID')
    parser.add_argument('--move', type=str, help='Delete the source file', default='True')

    args = parser.parse_args()

    CONFIG = {
        "class": args.class_name,
        "student_list": args.student_list,
        "folder_path": args.folder_path,
        "target_folder_path": args.target_folder_path,
        "course_name": "",  # course_name is optional and can be empty
        "student_num": args.student_num,
        "move": args.move.lower() == 'true',
    }

    name_id_dict = read_txt_file(CONFIG["student_list"])
    process_homework(CONFIG["folder_path"], CONFIG["target_folder_path"], CONFIG["course_name"], name_id_dict,CONFIG["class"])

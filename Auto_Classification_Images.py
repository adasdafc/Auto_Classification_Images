import json
import os
import shutil
import random

def distinguish_json_image(file_name):
    """区分JSON文件和图像文件"""
    if file_name.endswith(".json"):
        return "json"
    else:
        return "image"
def get_folder_path(src_folder):
    """读取输入的路径"""
    return src_folder

def record_data(src_folder, num_folders):
    """记录数据"""
    print(f"源文件夹: {src_folder}")
    print(f"目标文件夹数量: {num_folders}")

def read_num(num_folders_input):
    """读取int数据"""
    try:
        return int(num_folders_input)
    except ValueError:
        print("输入必须是整数.")
        return None

dest_folder_names = {
    2: ["CJ", "J"],
    3: ["CJ", "J", "quan"],
    4: ["CJ", "J", "quan", "yun"]
}

class InvalidDestinationFolderCount(ValueError):
    pass

def Create_top_level_folder(top_level_folder, prefix="folders_"):
    i = 1
    while True:
        folder_path = os.path.join(top_level_folder, f"{prefix}{i}")
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)

                return folder_path
            except OSError as e:
                return
        i += 1
def create_dest_folders(num_dest_folders, top_level_folder):
    dest_folders = []
    for folder_name in dest_folder_names[num_dest_folders]:
        folder_path = os.path.join(top_level_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        dest_folders.append(folder_path)
    return dest_folders

def split_images(src_folder, top_level_folder, num_folders, update_progress=None):
    """
    根据数据计算分类
    """
    if num_folders < 1 or num_folders > 4:
        raise ValueError("目标文件夹数量必须在 1 到 4 之间.")

    dest_folders = create_dest_folders(num_folders, top_level_folder)

    image_files = [f for f in os.listdir(src_folder) if distinguish_json_image(f) == "image"]
    total_image_files = len(image_files)

    # 按照给定的 num_folders 计算每个文件夹应该有的文件数量
    files_per_folder = total_image_files // num_folders
    remaining_files = total_image_files % num_folders

    # 将图像文件分配到目标文件夹
    for i, file_name in enumerate(image_files):
        dest_folder_index = i // files_per_folder
        if dest_folder_index >= num_folders:
            # 如果剩余文件不足一个完整的文件夹,则随机分配到目标文件夹
            dest_folder_index = random.randint(0, num_folders - 1)
        dest_folder = dest_folders[dest_folder_index]
        src_path = os.path.join(src_folder, file_name)
        dest_path = os.path.join(dest_folder, file_name)
        shutil.copy(src_path, dest_path)

    # 处理 JSON 文件
    json_files = [f for f in os.listdir(src_folder) if distinguish_json_image(f) == "json"]
    for file_name in json_files:
        src_path = os.path.join(src_folder, file_name)
        for image_file in image_files:
            image_base_name = os.path.splitext(image_file)[0]
            json_base_name = os.path.splitext(file_name)[0]
            if image_base_name == json_base_name:
                for i, dest_folder in enumerate(dest_folders):
                    if image_file in os.listdir(dest_folder):
                        dest_path = os.path.join(dest_folder, file_name)
                        shutil.copy(src_path, dest_path)
                        break

    print(f"图像文件和JSON文件已成功分割到 {top_level_folder}中的{num_folders} 个文件夹中.")
def create_copy(src_folder, dest_folder_path, num_dest_folders):
    """创建文件夹并分配图像"""
    split_images(src_folder, dest_folder_path, num_dest_folders)
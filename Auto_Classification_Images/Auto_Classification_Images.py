import os
import shutil
import random
import json

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

def create_dest_folders(num_dest_folders, dest_folder_path):
    dest_folders = []
    for folder_name in dest_folder_names[num_dest_folders]:
        folder_path = os.path.join(dest_folder_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        dest_folders.append(folder_path)
    return dest_folders

def split_images(src_folder, dest_folder_path, num_dest_folders, progress_callback=None):
    """
    根据数据计算分类
    """
    num_folders = read_num(num_dest_folders)
    if num_folders is None:
        return

    if num_folders < 1 or num_folders > 4:
        raise InvalidDestinationFolderCount("目标文件夹数量必须在 1 到 4 之间.")

    dest_folders = create_dest_folders(num_folders, dest_folder_path)

    total_files = len(os.listdir(src_folder))
    current_progress = 0

    for file_name in os.listdir(src_folder):
        file_type = distinguish_json_image(file_name)
        src_path = os.path.join(src_folder, file_name)
        if file_type == "image":
            dest_folder = dest_folders[random.randint(0, num_folders - 1)]
            dest_path = os.path.join(dest_folder, file_name)
            shutil.copy(src_path, dest_path)
        elif file_type == "json":
            # 找到同名的图像文件,并将JSON文件放到对应的文件夹中
            for image_file in os.listdir(src_folder):
                if image_file.endswith(".jpg") or image_file.endswith(".png"):
                    image_base_name = os.path.splitext(image_file)[0]
                    json_base_name = os.path.splitext(file_name)[0]
                    if image_base_name == json_base_name:
                        for i, dest_folder in enumerate(dest_folders):
                            if image_file in os.listdir(dest_folder):
                                dest_path = os.path.join(dest_folder, file_name)
                                shutil.copy(src_path, dest_path)
                                break
        current_progress += 1
        if progress_callback:
            progress_callback(int(current_progress / total_files * 100))
    print(f"图像文件和JSON文件已成功分割到 {dest_folder_path}中的{num_folders} 个文件夹中.")


def create_copy(src_folder, dest_folder_path, num_dest_folders):
    """创建文件夹并分配图像"""
    split_images(src_folder, dest_folder_path, num_dest_folders)
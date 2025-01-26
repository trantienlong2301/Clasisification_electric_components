import os

def list_files_in_directory(directory):
    """
    Liệt kê tất cả các file trong thư mục.

    Args:
        directory (str): Đường dẫn tới thư mục.

    Returns:
        list: Danh sách tên các file trong thư mục.
    """
    try:
        # Lấy danh sách các file trong thư mục
        files = os.listdir(directory)
        return files
    except FileNotFoundError:
        print(f"Thư mục '{directory}' không tồn tại.")
        return []
    except PermissionError:
        print(f"Không có quyền truy cập thư mục '{directory}'.")
        return []

def find_missing_files(directory, total_files):
    """
    Tìm các file bị thiếu trong thư mục.

    Args:
        directory (str): Đường dẫn tới thư mục chứa các file.
        total_files (int): Tổng số file dự kiến (1 đến total_files).

    Returns:
        list: Danh sách các file bị thiếu.
    """
    existing_files = list_files_in_directory(directory)
    existing_numbers = set(
        int(f.split('.')[0]) for f in existing_files if f.endswith('.txt') and f.split('.')[0].isdigit()
    )
    missing_files = [i for i in range(1, total_files + 1) if i not in existing_numbers]
    return missing_files

# Thư mục chứa các file
folder_path = "C:/Users/Admin/Desktop/1"

# Tổng số file dự kiến
total_files = 1450

# Tìm file bị thiếu
missing = find_missing_files(folder_path, total_files)

if missing:
    print("Các file bị thiếu:", missing)
else:
    print("Không có file nào bị thiếu.")
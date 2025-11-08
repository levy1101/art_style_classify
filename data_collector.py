import os
import shutil
import logging
from sklearn.model_selection import train_test_split

def create_directories(output_base_dir, styles):
    try:
        os.makedirs(output_base_dir, exist_ok=True)
        for split in ['train', 'validate', 'test']:
            os.makedirs(os.path.join(output_base_dir, split), exist_ok=True)
            for style in styles:
                os.makedirs(os.path.join(output_base_dir, split, style), exist_ok=True)
        print("Thư mục đã được tạo thành công.")
    except OSError as e:
        print(f"Lỗi khi tạo thư mục: {e}")

def split_data(main_dir, training_dir, validation_dir, test_dir, split_size, max_files=2000, random_seed=42):
    if not main_dir or not os.path.exists(main_dir):
        logging.error("Lỗi: main_dir không hợp lệ hoặc không tồn tại.")
        return
    if not (0 < split_size < 1):
        logging.error("Lỗi: split_size phải nằm giữa 0 và 1.")
        return
    os.makedirs(training_dir, exist_ok=True)
    os.makedirs(validation_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    all_files = [file for file in os.listdir(main_dir) if os.path.isfile(os.path.join(main_dir, file)) and os.path.getsize(os.path.join(main_dir, file)) > 0]
    if not all_files:
        logging.error("Lỗi: main_dir trống.")
        return
    if len(all_files) > max_files:
        all_files = all_files[:max_files]
        logging.info(f"Giới hạn {max_files} tệp từ tổng số {len(all_files)}.")
    train_files, remaining_files = train_test_split(all_files, train_size=split_size, random_state=random_seed)
    validation_files, test_files = train_test_split(remaining_files, test_size=0.5, random_state=random_seed)
    def copy_files(source_dir, destination_dir, file_list):
        for file in file_list:
            src_path = os.path.join(source_dir, file)
            dst_path = os.path.join(destination_dir, file)
            if not os.path.isfile(src_path):
                logging.warning(f"Bỏ qua không phải file: {file}")
                continue
            try:
                shutil.copyfile(src_path, dst_path)
            except Exception as e:
                logging.error(f"Lỗi sao chép {file}: {e}")
    copy_files(main_dir, training_dir, train_files)
    copy_files(main_dir, validation_dir, validation_files)
    copy_files(main_dir, test_dir, test_files)
    logging.info("Chia dữ liệu thành công!")

def collect_data_if_needed(output_base_dir, style_dirs, styles):
    # Kiểm tra nếu các thư mục train/validate/test đã có dữ liệu thì bỏ qua
    train_dir = os.path.join(output_base_dir, 'train')
    validate_dir = os.path.join(output_base_dir, 'validate')
    test_dir = os.path.join(output_base_dir, 'test')
    need_collect = False
    for split_dir in [train_dir, validate_dir, test_dir]:
        if not os.path.exists(split_dir) or not any(os.listdir(split_dir)):
            need_collect = True
    if not need_collect:
        print("Dữ liệu đã được chia, không cần collect lại.")
        return
    create_directories(output_base_dir, styles)
    for style, style_dir in style_dirs.items():
        split_data(
            style_dir,
            os.path.join(output_base_dir, f"train/{style}"),
            os.path.join(output_base_dir, f"validate/{style}"),
            os.path.join(output_base_dir, f"test/{style}"),
            0.8
        )

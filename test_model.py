#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script để kiểm tra và đánh giá mô hình phân loại phong cách nghệ thuật.
Dựa trên notebook gốc, tách riêng phần testing.
"""

import os
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from constants import WORKING_BASE_DIR, MODEL_FILENAME, LABELS_FILENAME

# Định nghĩa đường dẫn
OUTPUT_BASE_DIR = WORKING_BASE_DIR
MODEL_PATH = os.path.join(OUTPUT_BASE_DIR, MODEL_FILENAME)
LABELS_PATH = LABELS_FILENAME

# Tải mô hình đã huấn luyện
print("Đang tải mô hình...")
model = load_model(MODEL_PATH)
print("Mô hình đã được tải thành công.")

# Tạo test generator
test_gen = ImageDataGenerator(rescale=1./255.)

test_generator = test_gen.flow_from_directory(
    os.path.join(OUTPUT_BASE_DIR, 'test'),
    target_size=(256, 256),
    batch_size=64,
    shuffle=False,
    class_mode="categorical"
)

# Đánh giá mô hình trên tập validation (để so sánh)
validation_gen = ImageDataGenerator(rescale=1./255.)
validation_generator = validation_gen.flow_from_directory(
    os.path.join(OUTPUT_BASE_DIR, 'validate'),
    target_size=(256, 256),
    batch_size=64,
    shuffle=False,
    class_mode="categorical"
)

print("Đánh giá trên tập validation:")
loss, accuracy = model.evaluate(validation_generator)
print(f"Độ chính xác: {accuracy:.4f}")
print(f"Mất mát: {loss:.4f}")

# Dự đoán trên tập test
print("Đang dự đoán trên tập test...")
y_pred_prob = model.predict(test_generator)
y_pred = np.argmax(y_pred_prob, axis=1)
y_true = test_generator.classes

# Báo cáo phân loại
class_labels = list(test_generator.class_indices.keys())
report = classification_report(y_true, y_pred, target_names=class_labels)
print("Báo cáo phân loại:")
print(report)

# Ma trận nhầm lẫn
conf_matrix = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=class_labels, yticklabels=class_labels)
plt.xlabel('Nhãn dự đoán')
plt.ylabel('Nhãn thực tế')
plt.title('Ma trận nhầm lẫn')
plt.show()

# Hàm hiển thị lưới ảnh với dự đoán
def display_image_grid(model, n=9, num_cols=3):
    """
    Hiển thị lưới ảnh với phong cách thực tế và dự đoán.

    Tham số:
    model (tf.keras.Model): Mô hình đã huấn luyện để dự đoán phong cách ảnh.
    n (int): Số lượng ảnh để hiển thị. Mặc định là 9.
    num_cols (int): Số cột trong lưới. Mặc định là 3.
    """
    num_rows = (n + num_cols - 1) // num_cols

    test_images_dir = os.path.join(OUTPUT_BASE_DIR, 'test')

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 12))

    for i in range(n):
        row = i // num_cols
        col = i % num_cols

        # Chọn ngẫu nhiên một phong cách và một ảnh trong phong cách đó
        random_style = random.choice(os.listdir(test_images_dir))
        random_image = random.choice(os.listdir(os.path.join(test_images_dir, random_style)))
        random_image_file = os.path.join(test_images_dir, random_style, random_image)

        # Tải và tiền xử lý ảnh
        test_image = image.load_img(random_image_file, target_size=(256, 256))
        test_image_array = image.img_to_array(test_image) / 255.
        test_image_array = np.expand_dims(test_image_array, axis=0)

        # Dự đoán phong cách nghệ thuật
        prediction = model.predict(test_image_array)
        prediction_probability = np.amax(prediction)
        prediction_idx = np.argmax(prediction)

        # Lấy nhãn từ generator
        labels = {v: k for k, v in test_generator.class_indices.items()}

        # Kiểm tra xem dự đoán có đúng không
        actual_style = random_style.replace('_', ' ')
        predicted_style = labels[prediction_idx].replace('_', ' ')
        is_correct = actual_style == predicted_style
        title_color = 'green' if is_correct else 'red'

        # Tạo tiêu đề với phong cách thực tế và dự đoán
        title = f"Phong cách thực tế = {actual_style}\n" \
                f"Phong cách dự đoán = {predicted_style}\n" \
                f"Xác suất dự đoán = {prediction_probability * 100:.2f}%"

        # Hiển thị ảnh với tiêu đề
        if num_rows > 1:
            ax = axes[row, col]
        else:
            ax = axes[col]
        ax.imshow(plt.imread(random_image_file))
        ax.set_title(title, color=title_color, fontsize=8)
        ax.axis('off')

    plt.tight_layout()
    plt.show()

# Hiển thị ví dụ dự đoán
print("Hiển thị ví dụ dự đoán trên 4 ảnh:")
display_image_grid(model, n=4, num_cols=2)

print("Hoàn thành kiểm tra mô hình!")
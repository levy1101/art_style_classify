#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script để huấn luyện mô hình phân loại phong cách nghệ thuật.
Dựa trên notebook gốc, tách riêng phần training.
"""

import numpy as np
import pandas as pd
import os
import shutil
from sklearn.model_selection import train_test_split
import logging
from tensorflow.python.client import device_lib

print("Danh sách thiết bị TensorFlow nhận diện:")
for device in device_lib.list_local_devices():
    print(device)
import sys
from datetime import datetime
from constants import DATA_BASE_DIR, WORKING_BASE_DIR, LOG_DIR, MODEL_FILENAME, STYLE_CLASSES

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, AveragePooling2D, Dropout, GlobalAveragePooling2D, GlobalMaxPooling2D, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import SGD
import matplotlib.pyplot as plt
import keras
from tensorflow.keras.applications.vgg16 import VGG16
import keras_tuner as kt
from tensorflow.keras.applications import ResNet50, InceptionV3, DenseNet121, Xception, EfficientNetB1
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.metrics import Precision, Recall, F1Score
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tensorflow.keras.preprocessing import image
import os
from glob import glob
import shutil
import random
from shutil import copyfile


# Tạo tên file log theo thời gian
os.makedirs(LOG_DIR, exist_ok=True)
session_time = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(LOG_DIR, f'session_{session_time}.txt')

# Cấu hình logging ra file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Ghi lại các print ra file log
class LoggerWriter:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
    def write(self, message):
        message = message.strip()
        if message:
            self.logger.log(self.level, message)
    def flush(self):
        pass
sys.stdout = LoggerWriter(logging.getLogger(), logging.INFO)
sys.stderr = LoggerWriter(logging.getLogger(), logging.ERROR)

OUTPUT_BASE_DIR = WORKING_BASE_DIR

try:
    from data_collector import collect_data_if_needed
    style_dirs = {style: os.path.join(DATA_BASE_DIR, f'wikiart/{style}') for style in STYLE_CLASSES}
    collect_data_if_needed(OUTPUT_BASE_DIR, style_dirs, STYLE_CLASSES)
except ImportError:
    print("Không tìm thấy data_collector, chỉ sử dụng dữ liệu đã chia sẵn.")
train_gen = ImageDataGenerator(
    rescale=1./255.,
    width_shift_range=0.1,
    height_shift_range=0.1,
    fill_mode='nearest'
)

validation_gen = ImageDataGenerator(rescale=1./255.)

train_generator = train_gen.flow_from_directory(
    os.path.join(OUTPUT_BASE_DIR, 'train'),
    target_size=(256, 256),
    batch_size=64,
    class_mode="categorical"
)

validation_generator = validation_gen.flow_from_directory(
    os.path.join(OUTPUT_BASE_DIR, 'validate'),
    target_size=(256, 256),
    batch_size=64,
    class_mode="categorical"
)

# Xây dựng mô hình
base_model = Xception(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
for layer in base_model.layers:
    layer.trainable = False

model = Sequential()
model.add(base_model)
model.add(GlobalAveragePooling2D())
model.add(Dense(1024, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Dense(5, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print("Tóm tắt mô hình ban đầu:")
model.summary()

# Callbacks
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3)

# Huấn luyện giai đoạn 1
print("Bắt đầu huấn luyện giai đoạn 1...")
result1 = model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator
)

# Mở khóa một số lớp cuối
for layer in base_model.layers[-35:]:
    layer.trainable = True

# Biên dịch lại với learning rate thấp hơn
model.compile(optimizer=optimizers.Adam(learning_rate=1e-4), loss='categorical_crossentropy', metrics=['accuracy'])
print("Tóm tắt mô hình sau khi fine-tune:")
model.summary()

# Huấn luyện giai đoạn 2
print("Bắt đầu huấn luyện giai đoạn 2 (fine-tuning)...")
result2 = model.fit(
    train_generator,
    epochs=50,
    callbacks=[reduce_lr, early_stop],
    validation_data=validation_generator
)

# Lưu mô hình
model.save(os.path.join(OUTPUT_BASE_DIR, MODEL_FILENAME))
print(f"Mô hình đã được lưu tại {os.path.join(OUTPUT_BASE_DIR, MODEL_FILENAME)}")
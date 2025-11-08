# Phân Loại Phong Cách Nghệ Thuật Sử Dụng Học Sâu

Dự án này triển khai một hệ thống phân loại phong cách nghệ thuật sử dụng mạng nơ-ron tích chập (CNN) dựa trên mô hình Xception đã được huấn luyện trước trên tập dữ liệu ImageNet. Hệ thống có thể phân loại ảnh nghệ thuật thành 5 phong cách chính: Baroque, Expressionism, Cubism, Japanese Art, và Art Nouveau Modern.

## Tổng Quan

### Mục Tiêu Dự Án

- Xây dựng mô hình học máy có khả năng nhận diện và phân loại phong cách nghệ thuật từ hình ảnh.
- Sử dụng kỹ thuật transfer learning để cải thiện hiệu suất với dữ liệu hạn chế.
- Triển khai mô hình có thể sử dụng trên các thiết bị di động thông qua TensorFlow Lite.

### Kiến Trúc Mô Hình

- **Mô hình cơ sở**: Xception (pre-trained trên ImageNet)
- **Lớp bổ sung**:
  - Global Average Pooling
  - Dense layer (1024 neurons, ReLU activation)
  - Batch Normalization
  - Dropout (0.2)
  - Dense layer (5 neurons, Softmax activation)

### Quy Trình Huấn Luyện

1. **Chuẩn bị dữ liệu**: Chia tập dữ liệu WikiArt thành train/validation/test (80%/10%/10%)
2. **Tiền xử lý**: Resize ảnh về 256x256, augmentation (shift, rescale)
3. **Huấn luyện giai đoạn 1**: Freeze base model, train top layers
4. **Fine-tuning**: Unfreeze 35 layers cuối, train với learning rate thấp hơn
5. **Đánh giá**: Accuracy, loss, classification report, confusion matrix

## Yêu Cầu Hệ Thống

### Thư Viện Python

```
tensorflow>=2.0
keras
numpy
pandas
scikit-learn
matplotlib
seaborn
Pillow
```

### Dữ Liệu

- Tập dữ liệu WikiArt với các phong cách nghệ thuật
- Cấu trúc thư mục:

  ```
  /kaggle/input/
  ├── wikiart/
  │   ├── Baroque/
  │   ├── Expressionism/
  │   ├── Cubism/
  │   └── Art_Nouveau_Modern/
  └── wikiart-art-movementsstyles/
      └── Japanese_Art/
          └── Japanese_Art/
  ```

## Cách Sử Dụng

### 1. Huấn Luyện Mô Hình (`train_model.py`)

#### Chuẩn Bị

- Đảm bảo có tập dữ liệu WikiArt trong thư mục `/kaggle/input/`
- Thay đổi `DATA_BASE_DIR` và `OUTPUT_BASE_DIR` nếu cần

#### Chạy Script

```bash
python train_model.py
```

#### Đầu Ra

- Thư mục dữ liệu đã chia: `/kaggle/working/art_styles/`
- Mô hình đã huấn luyện: `/kaggle/working/art_style_classifier.h5`
- Logs huấn luyện với accuracy và loss

#### Thời Gian Ước Tính

- Chuẩn bị dữ liệu: 5-10 phút
- Huấn luyện: 2-4 giờ (tùy thuộc vào GPU)

### 2. Kiểm Tra Mô Hình (`test_model.py`)

#### Chuẩn Bị

- Chạy `train_model.py` trước để có mô hình đã huấn luyện
- Đảm bảo có thư mục test data

#### Chạy Script

```bash
python test_model.py
```

#### Đầu Ra

- Độ chính xác và mất mát trên tập validation
- Báo cáo phân loại chi tiết
- Ma trận nhầm lẫn (confusion matrix)
- Lưới ảnh mẫu với dự đoán
- Mô hình TensorFlow Lite: `style_model.tflite`
- File nhãn: `labels.txt`

## Giải Thích Chi Tiết

### Chuẩn Bị Dữ Liệu

Script tự động tạo cấu trúc thư mục và chia dữ liệu:

- **Train**: 80% dữ liệu cho huấn luyện
- **Validation**: 10% cho validation trong quá trình train
- **Test**: 10% cho đánh giá cuối cùng

Mỗi phong cách được giới hạn tối đa 2000 ảnh để cân bằng.

### Tiền Xử Lý

- **Rescaling**: Chia cho 255 để normalize về [0,1]
- **Augmentation**: Shift ngang/dọc 10% để tăng đa dạng dữ liệu
- **Resize**: Tất cả ảnh về 256x256 pixels

### Mô Hình

Xception là mô hình hiệu quả cho classification, với depthwise separable convolutions giảm tham số nhưng giữ độ chính xác.

**Lý do chọn Xception**:

- Hiệu suất cao trên ImageNet
- Ít tham số hơn các mô hình khác
- Tốt cho transfer learning

### Huấn Luyện

**Giai đoạn 1**: Chỉ train top layers, base model freeze để tránh overfitting.

**Giai đoạn 2**: Fine-tune bằng cách unfreeze một số layers cuối, với learning rate thấp hơn.

**Callbacks**:

- Early Stopping: Dừng nếu validation loss không cải thiện sau 10 epochs
- Reduce LR: Giảm learning rate nếu validation loss không cải thiện sau 3 epochs

### Đánh Giá

- **Accuracy/Loss**: Metrics cơ bản
- **Classification Report**: Precision, Recall, F1-score cho từng class
- **Confusion Matrix**: Hiển thị lỗi phân loại giữa các classes
- **Visual Examples**: Hiển thị ảnh mẫu với dự đoán để kiểm tra trực quan

### Triển Khai

Mô hình được chuyển đổi sang TensorFlow Lite để sử dụng trên mobile/web. File `labels.txt` chứa mapping từ index sang tên phong cách.

## Kết Quả Mong Đợi

Với tập dữ liệu đầy đủ, mô hình có thể đạt:

- Accuracy: 85-95% trên tập test
- Precision/Recall: Cao cho các phong cách có nhiều đặc trưng rõ ràng
- Thời gian inference: <100ms/ảnh trên GPU

## Ghi Chú

- Script được thiết kế chạy trên Kaggle environment
- Có thể cần điều chỉnh đường dẫn cho môi trường khác
- Để cải thiện hiệu suất, có thể thử các mô hình khác như EfficientNet hoặc ResNet
- Thêm data augmentation hoặc sử dụng larger dataset có thể cải thiện accuracy

## Liên Hệ

Nếu có câu hỏi hoặc cần hỗ trợ, vui lòng kiểm tra code và comments trong script.

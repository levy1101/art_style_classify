# Art Style Classifier - Web App

Ứng dụng web đơn giản sử dụng AI để nhận diện phong cách nghệ thuật từ ảnh và tạo prompt cho Stable Diffusion.

## Tính năng

### 1. Style Hunter - Nhận diện phong cách từ ảnh

- **Input**: Upload một bức ảnh bất kỳ
- **Xử lý**: AI phân tích phong cách nghệ thuật
- **Output**: Một prompt duy nhất chứa tất cả thông số
  - **Ví dụ**: "(masterpiece, best quality, high detail), Baroque style, dramatic lighting, sharp focus — Steps:20, Sampler:Euler a, CFG:7, Size:512x512, Negative:(worst quality, low quality, blurry, bad anatomy, deformed, extra limbs, watermark, text)"

### 2. Style Remix - Phối lại phong cách vào nội dung mới

- **Input**:
  - Upload ảnh mẫu (để lấy phong cách)
  - Nhập nội dung muốn vẽ (ví dụ: "con mèo đang ngủ")
- **Xử lý**: AI lấy phong cách từ ảnh mẫu + áp dụng vào nội dung mới
- **Output**: Một prompt duy nhất kết hợp nội dung và phong cách
  - **Ví dụ**: "(masterpiece, best quality, high detail), a sleeping cat, Baroque style, dramatic lighting, sharp focus — Steps:20, Sampler:Euler a, CFG:7, Size:512x512, Negative:(worst quality, low quality, blurry, bad anatomy, deformed, extra limbs, watermark, text)"

## Phong cách nghệ thuật hỗ trợ

1. Art Nouveau Modern
2. Baroque
3. Cubism
4. Expressionism
5. Japanese Art

## Cài đặt và chạy

```bash
git clone <repository-url>
cd art_style_classify
pip install -r requirements.txt
python app.py
```

Ứng dụng sẽ chạy trên `http://localhost:5000`

## Công nghệ sử dụng

- **Backend**: Python + Flask
- **AI Models**:
  - TensorFlow/Keras (phân loại phong cách nghệ thuật - `art_style_classifier.h5`)
  - ChatGPT API (tạo prompt theo template)
- **Frontend**: HTML/CSS/JavaScript đơn giản

## API ChatGPT Template

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "Sinh 1 prompt duy nhất theo cấu trúc: (masterpiece, best quality, high detail), {CONTENT}, {STYLE}, dramatic lighting, sharp focus — Steps:20, Sampler:Euler a, CFG:7, Size:512x512, Negative:(worst quality, low quality, blurry, bad anatomy, deformed, extra limbs, watermark, text). Không thêm giải thích."
    },
    {
      "role": "user",
      "content": "CONTENT=a sleeping cat, STYLE=Baroque style"
    }
  ]
}
```

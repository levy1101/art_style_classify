# 🎨 Prompt-Hunter - AI Art Style Classifier & Prompt Generator

Ứng dụng web thông minh sử dụng AI để nhận diện phong cách nghệ thuật từ ảnh và tạo prompt tối ưu cho các công cụ vẽ AI như Stable Diffusion, Midjourney.

## ✨ Tính năng chính

### 1. 🎯 Style Hunter - Nhận diện phong cách từ ảnh

**Luồng sử dụng:**
1. Upload ảnh mẫu
2. AI phân tích phong cách tự động
3. Nhận prompt có sẵn chứa phong cách

**Ví dụ Output:**
```
(masterpiece, best quality, high detail), Baroque, dramatic lighting, sharp focus — 
Steps:20, Sampler:Euler a, CFG:7, Size:512x512, 
Negative:(worst quality, low quality, blurry, bad anatomy, deformed, extra limbs, watermark, text)
```

---

### 2. 🔄 Style Remix - Kết hợp phong cách + nội dung mới

**Luồng sử dụng:**
1. Upload ảnh để lấy phong cách
2. AI phân tích phong cách
3. Nhập nội dung muốn vẽ (ví dụ: "robot samurai")
4. **Check Content** - AI kiểm tra xem nội dung có phù hợp với style không
   - ✅ **Nếu phù hợp**: Xác nhận nội dung
   - ❌ **Nếu không phù hợp**: AI gợi ý nội dung liên quan hơn (ví dụ: "samurai cyborg warrior")
5. **Gen Prompt** - Tạo prompt kết hợp nội dung + phong cách
6. Nhận prompt tối ưu

**Ví dụ Flow:**
- Input: "robot" + "Japanese Art"
- Check: ❌ Không liên quan
- Gợi ý: "samurai cyborg" 
- Output Prompt: 
```
(masterpiece, best quality, high detail), samurai cyborg, Japanese Art, dramatic lighting...
```

---

## 🎨 Phong cách nghệ thuật hỗ trợ

1. **Art Nouveau Modern** - Phong cách hiện đại trang nhã
2. **Baroque** - Phong cách lịch sử phát triển
3. **Cubism** - Phong cách trừu tượng hình học
4. **Expressionism** - Phong cách biểu cảm sắc nét
5. **Japanese Art** - Phong cách Nhật Bản truyền thống

---

## 🚀 Cài đặt & Chạy

### Yêu cầu
- Python 3.8+
- Groq API Key (free tier có sẵn)

### Hướng dẫn

```bash
# Clone repository
git clone <repository-url>
cd art_style_classify

# Cài đặt dependencies
pip install -r requirements.txt

# Thiết lập API Key
# Tạo file .env và thêm:
# GROQ_API_KEY=your_api_key_here

# Chạy ứng dụng
python app.py
```

Truy cập: `http://localhost:5000`

---

## 🛠 Công nghệ sử dụng

### Backend
- **Framework**: Flask (Python)
- **AI Models**:
  - **TensorFlow/Keras**: Phân loại phong cách nghệ thuật (`art_style_classifier.h5`)
  - **Groq API**: LLaMA 3.1 8B - Tạo prompt + kiểm tra nội dung
- **Image Processing**: Pillow, NumPy

### Frontend
- **HTML5/CSS3/JavaScript** (Bootstrap 5 framework)
- **Drag & Drop** hỗ trợ upload ảnh
- **Responsive Design** tối ưu cho mobile + desktop

---

## 📁 Cấu trúc dự án

```
art_style_classify/
├── app.py                          # Flask app chính
├── constants.py                    # Hằng số + API prompts
├── requirements.txt                # Dependencies
├── art_style_classifier.h5        # Mô hình TensorFlow
├── templates/
│   └── index.html                 # Frontend UI
├── static/
│   └── uploads/                   # Thư mục lưu ảnh upload
├── kaggle/
│   └── input/wikiart/            # Dataset training (nếu cần retrain)
└── README.md
```

---

## 🔧 API Endpoints

### 1. `/predict` (POST)
Phân tích phong cách từ ảnh

**Request:**
```json
{
  "file": "<image_file>"
}
```

**Response:**
```json
{
  "style": "Japanese Art",
  "confidence": "95.23%"
}
```

### 2. `/suggest-content` (POST)
Kiểm tra nội dung và gợi ý nếu cần

**Request:**
```json
{
  "content": "robot",
  "style": "Japanese Art"
}
```

**Response:**
```json
{
  "is_relevant": false,
  "suggested_content": "samurai cyborg warrior"
}
```

### 3. `/generate-full-prompt` (POST)
Tạo prompt hoàn chỉnh

**Request:**
```json
{
  "content": "samurai cyborg",
  "style": "Japanese Art"
}
```

**Response:**
```json
{
  "prompt": "(masterpiece, best quality, high detail), samurai cyborg, Japanese Art, dramatic lighting, sharp focus — Steps:20, Sampler:Euler a, CFG:7, Size:512x512, Negative:(worst quality, low quality, blurry, bad anatomy, deformed, extra limbs, watermark, text)"
}
```

---

## 💡 Cách hoạt động

### 1. Style Detection (TensorFlow)
```
Input Image → Resize (256x256) → Normalize → CNN Model → Prediction → Style Label
```

### 2. Content Relevance Check (Groq LLM)
```
Content + Style → LLM Evaluation (English prompt) → YES/NO response
→ If NO: Suggest related content
```

### 3. Prompt Generation (Groq LLM)
```
Content + Style → LLM with System Prompt → Optimized Prompt for Stable Diffusion
```

---

## 📝 Ví dụ sử dụng

### Scenario 1: Style Hunter
```
User: Upload "Mona Lisa.jpg"
AI detects: Baroque style
Output: "(masterpiece, best quality, high detail), Baroque, dramatic lighting..."
User: Copy prompt → Use in Midjourney/Stable Diffusion
```

### Scenario 2: Style Remix  
```
User: Upload "Van Gogh Starry Night.jpg" + Input "robot ninja"
AI detects: Expressionism
Content Check: robot + Expressionism = NO match
AI suggests: "geometric ninja warrior"
User accepts suggestion
Output: "(masterpiece, best quality, high detail), geometric ninja warrior, Expressionism..."
User: Copy → Generate image
```

---

## 🔐 Biến môi trường

```bash
# .env file
GROQ_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Lấy API Key miễn phí tại: https://console.groq.com/

---

## 📊 Hiệu suất

- **Style Detection**: ~92-95% (5 phong cách)
- **Content Relevance**: ~88-92% (dựa trên LLM evaluation)

---

## 🐛 Khắc phục sự cố

### Lỗi "Model not loaded"
```bash
# Đảm bảo file art_style_classifier.h5 có trong thư mục gốc
ls art_style_classifier.h5
```

### Lỗi "Invalid API Key"
```bash
# Kiểm tra .env file
cat .env
# Lấy key mới từ https://console.groq.com/
```

### Ảnh upload lớn
- Giới hạn: 10MB
- Format: JPG, PNG

---

## 📚 Tài liệu tham khảo

- [Groq API Docs](https://console.groq.com/docs)
- [TensorFlow Keras](https://keras.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Stable Diffusion Prompting Guide](https://huggingface.co/docs/diffusers)

---

## 👨‍💻 Phát triển & Đóng góp

**Tính năng lên kế hoạch:**
- [ ] Hỗ trợ thêm phong cách nghệ thuật
- [ ] Lịch sử prompt đã tạo
- [ ] Export/Save prompt settings
- [ ] Batch processing nhiều ảnh
- [ ] Integration với Stable Diffusion API

---

## 📄 License

MIT License - Tự do sử dụng cho mục đích cá nhân & thương mại

---

**Được tạo với ❤️ để giúp cộng đồng AI Art**

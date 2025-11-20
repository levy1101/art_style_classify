from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
from openai import OpenAI
import google.genai as genai
from google.genai import types
from constants import MODEL_FILENAME, LABELS, GROQ_MODEL, SYSTEM_PROMPT, IMAGE_SIZE, GROQ_API_KEY, RELEVANCE_CHECK_PROMPT, CONTENT_SUGGESTION_PROMPT, GOOGLE_API_KEY

app = Flask(__name__)

# Load model globally
model = None
def load_model():
    global model
    if model is None:
        try:
            model = tf.keras.models.load_model(MODEL_FILENAME)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
    return model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Detect art style from image"""
    try:
        # Get form data
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'})

        # Validate file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({'error': 'Only PNG and JPG files are allowed'})

        # Load model
        model = load_model()
        if model is None:
            return jsonify({'error': 'Model not loaded'})

        # Process image
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        image = image.resize(IMAGE_SIZE)
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        # Predict
        predictions = model.predict(image_array)
        predicted_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_index])
        predicted_style = LABELS[predicted_index]

        # Return style only (not prompt yet)
        return jsonify({
            'style': predicted_style,
            'confidence': f'{confidence:.2%}'
        })

    except Exception as e:
        print(f"Error in predict: {e}")
        return jsonify({'error': 'Prediction failed'})

@app.route('/suggest-content', methods=['POST'])
def suggest_content():
    """Suggest content based on style"""
    try:
        style = request.json.get('style', '').strip()
        user_content = request.json.get('content', '').strip()

        if not style:
            return jsonify({'error': 'Missing style'})

        # If user content provided, check relevance
        if user_content:
            is_relevant, suggested_content = check_content_relevance_and_suggest(user_content, style)
            return jsonify({
                'is_relevant': is_relevant,
                'suggested_content': suggested_content if not is_relevant else None
            })
        else:
            return jsonify({'is_relevant': True, 'suggested_content': None})

    except Exception as e:
        print(f"Error in suggest_content: {e}")
        return jsonify({'error': 'Suggestion failed'})

@app.route('/generate-full-prompt', methods=['POST'])
def generate_full_prompt():
    """Generate complete prompt with content and style"""
    try:
        content = request.json.get('content', '').strip()
        style = request.json.get('style', '').strip()

        if not style:
            return jsonify({'error': 'Missing style'})

        # Generate prompt using Groq
        prompt = generate_groq_prompt(content, style)

        return jsonify({
            'prompt': prompt
        })

    except Exception as e:
        print(f"Error in generate_full_prompt: {e}")
        return jsonify({'error': 'Generation failed'})

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate images using Imagen API"""
    try:
        prompt = request.json.get('prompt', '').strip()

        if not prompt:
            return jsonify({'error': 'Missing prompt'})

        if not GOOGLE_API_KEY:
            return jsonify({'error': 'Google API key not configured'})

        # Set API key in environment
        os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
        client = genai.Client()

        response = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=4,
            )
        )

        images = []
        for generated_image in response.generated_images:
            # Convert bytes to base64 string
            import base64
            image_b64 = base64.b64encode(generated_image.image.image_bytes).decode('utf-8')
            images.append(f"data:image/png;base64,{image_b64}")

        return jsonify({'images': images})

    except Exception as e:
        print(f"Error generating image: {e}")
        return jsonify({'error': 'Image generation failed'})

def check_content_relevance(content, style):
    """Check if content and style are relevant, suggest bridging prompt if not"""
    try:
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        # First, check relevance
        relevance_prompt = f"""Bạn là một chuyên gia về nghệ thuật AI. Hãy kiểm tra xem nội dung "{content}" và phong cách "{style}" có liên quan hay phù hợp với nhau không?
        
Trả lời CHỈ "YES" hoặc "NO":
- YES nếu chúng liên quan tốt (ví dụ: "samurai" + "Japanese Art")
- NO nếu chúng không liên quan lắm (ví dụ: "robot" + "Baroque")"""

        relevance_response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "user", "content": relevance_prompt}
            ],
            max_tokens=10,
            temperature=0
        )

        is_relevant = "YES" in relevance_response.choices[0].message.content.upper()

        # If not relevant, suggest bridging prompt
        suggested_prompt = None
        if not is_relevant:
            suggestion_system = """Bạn là một chuyên gia tạo prompt cho Stable Diffusion.

TASK: Tạo prompt kết nối nội dung và phong cách.

Khi nội dung và phong cách không liên quan, hãy tạo prompt tạo cầu nối giữa chúng.
Ví dụ:
- CONTENT="robot", STYLE="Japanese Art" → "(masterpiece, best quality, high detail), robot in Japanese anime style, samurai cyborg fusion, Japanese Art, dramatic lighting..."
- CONTENT="thêm mèo con", STYLE="Baroque" → "(masterpiece, best quality, high detail), adorable kittens in ornate Baroque garden setting, romantic and regal, Baroque, dramatic lighting..."

INSTRUCTIONS:
- Tạo cầu nối tự nhiên giữa nội dung và phong cách
- Output ONLY the complete prompt, no explanations"""

            suggestion_user = f"CONTENT=\"{content}\", STYLE=\"{style}\""

            suggestion_response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": suggestion_system},
                    {"role": "user", "content": suggestion_user}
                ],
                max_tokens=200,
                temperature=0.1
            )

            suggested_prompt = suggestion_response.choices[0].message.content.strip()

        return is_relevant, suggested_prompt

    except Exception as e:
        print(f"Error checking relevance: {e}")
        return True, None  # Default to relevant if error

def check_content_relevance_and_suggest(content, style):
    """Check relevance and suggest alternative content if needed"""
    try:
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        # Check relevance using strict prompt
        relevance_response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": RELEVANCE_CHECK_PROMPT},
                {"role": "user", "content": f'CONTENT="{content}", STYLE="{style}"'}
            ],
            max_tokens=5,
            temperature=0
        )

        response_text = relevance_response.choices[0].message.content.strip().upper()
        print(f"[DEBUG] Relevance check - Content: '{content}', Style: '{style}'")
        print(f"[DEBUG] API Response: '{response_text}'")
        
        is_relevant = response_text == "YES"

        # If not relevant, suggest alternative content
        suggested_content = None
        if not is_relevant:
            suggestion_response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": CONTENT_SUGGESTION_PROMPT},
                    {"role": "user", "content": f'ORIGINAL="{content}", STYLE="{style}"'}
                ],
                max_tokens=50,
                temperature=0.1
            )

            suggested_content = suggestion_response.choices[0].message.content.strip()
            print(f"[DEBUG] Suggested content: '{suggested_content}'")

        return is_relevant, suggested_content

    except Exception as e:
        print(f"Error checking content relevance: {e}")
        import traceback
        traceback.print_exc()
        return False, None  # Default to NOT relevant if error (safer)

def generate_groq_prompt(content, style):
    """Generate prompt using Groq API (free tier)"""
    try:
        # Prepare content for template
        if content:
            content_part = content
        else:
            content_part = ""  # Empty for style hunter mode

        user_content = f"CONTENT={content_part}, STYLE={style}"

        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            max_tokens=200,
            temperature=0.1  # Low temperature for consistent output
        )

        prompt = response.choices[0].message.content.strip()
        return prompt

    except Exception as e:
        print(f"Groq API error: {e}")
        # Fallback prompt
        if content:
            return f"(masterpiece, best quality, high detail), {content}, {style}, dramatic lighting, sharp focus — Steps:20, Sampler:Euler a, CFG:7, Size:512x512, Negative:(worst quality, low quality, blurry, bad anatomy, deformed, extra limbs, watermark, text)"
        else:
            return f"(masterpiece, best quality, high detail), {style}, dramatic lighting, sharp focus — Steps:20, Sampler:Euler a, CFG:7, Size:512x512, Negative:(worst quality, low quality, blurry, bad anatomy, deformed, extra limbs, watermark, text)"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
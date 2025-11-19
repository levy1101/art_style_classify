from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
from openai import OpenAI
from constants import MODEL_FILENAME, LABELS, GROQ_MODEL, SYSTEM_PROMPT, IMAGE_SIZE, GROQ_API_KEY

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
    try:
        # Get form data
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})

        file = request.files['file']
        mode = request.form.get('mode', 'hunter')
        content = request.form.get('content', '').strip()

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

        # Generate prompt based on mode
        if mode == 'remix' and content:
            # Use Groq API for remix mode
            prompt = generate_groq_prompt(content, predicted_style)
        else:
            # Style Hunter mode - use detected style as content
            prompt = generate_groq_prompt("", predicted_style)

        return jsonify({
            'style': predicted_style,
            'confidence': f'{confidence:.2%}',
            'prompt': prompt
        })

    except Exception as e:
        print(f"Error in predict: {e}")
        return jsonify({'error': 'Prediction failed'})

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
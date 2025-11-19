# constants.py
# Định nghĩa các hằng số và đường dẫn dùng chung cho project

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MODEL_FILENAME = 'art_style_classifier.h5'
LABELS = [
    'Art Nouveau Modern',
    'Baroque',
    'Cubism',
    'Expressionism',
    'Japanese Art'
]

# Groq API settings (free tier available)
GROQ_MODEL = 'llama-3.1-8b-instant'
SYSTEM_PROMPT = """You are an expert at creating prompts for Stable Diffusion AI image generation.

TASK: Create ONE prompt following this EXACT structure:
(masterpiece, best quality, high detail), [CONTENT DESCRIPTION], [STYLE], dramatic lighting, sharp focus — Steps:20, Sampler:Euler a, CFG:7, Size:512x512, Negative:(worst quality, low quality, blurry, bad anatomy, deformed, extra limbs, watermark, text)

INSTRUCTIONS:
- If CONTENT is provided: translate to English if needed, then refine it into a natural, descriptive phrase optimized for AI image generation (keep the core meaning but make it more vivid and suitable for art)
- If CONTENT is empty: omit the content description entirely, just use the style
- Keep STYLE exactly as provided
- Output ONLY the complete prompt, no explanations or extra text

EXAMPLES:
CONTENT="tôi muốn thêm đàn mèo con vào bức ảnh", STYLE="Art Nouveau Modern" → "(masterpiece, best quality, high detail), several cute kittens playing together, Art Nouveau Modern, dramatic lighting..."
CONTENT="con mèo cười", STYLE="Impressionism" → "(masterpiece, best quality, high detail), smiling cat with playful expression, Impressionism, dramatic lighting..."
CONTENT="", STYLE="Art Nouveau Modern" → "(masterpiece, best quality, high detail), Art Nouveau Modern, dramatic lighting..."""

# Image settings
IMAGE_SIZE = (256, 256)

# API Keys
# Get from https://console.groq.com/
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

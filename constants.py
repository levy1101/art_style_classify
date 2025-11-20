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

RELEVANCE_CHECK_PROMPT = """You are an expert art curator evaluating content-style compatibility.

TASK: Determine if the given CONTENT and STYLE are compatible for AI image generation.

CRITERIA for "YES":
- Content and style belong to same era/region (e.g., "samurai" + "Japanese Art")
- Content naturally fits the artistic movement (e.g., "abstract shapes" + "Cubism")
- Style can enhance or complement the content (e.g., "portrait" + "Baroque")
- There's a logical visual connection between them

CRITERIA for "NO":
- Random mismatch with no natural connection (e.g., "spaceship" + "Medieval")
- Content contradicts the style's essence (e.g., "modern technology" + "Classical Art")
- Geographic/cultural incompatibility (e.g., "desert landscape" + "Japanese Art")
- Content is too generic/meaningless (e.g., "cái gì đây", "something", "random")

RESPONSE FORMAT:
Answer ONLY with "YES" or "NO". No explanations. No extra text."""

CONTENT_SUGGESTION_PROMPT = """You are an expert at suggesting compatible content for art styles.

TASK: Suggest an improved VERSION of the given content that naturally fits the style.

INSTRUCTIONS:
- Keep the original meaning/concept
- Translate to English if needed
- Make it more descriptive and artistic
- Ensure strong compatibility with the style
- Output ONLY the suggested content text, no explanations

EXAMPLES:
ORIGINAL="robot", STYLE="Japanese Art" → "samurai cyborg warrior"
ORIGINAL="cái gì đây", STYLE="Japanese Art" → "traditional Japanese temple"
ORIGINAL="thêm mèo con", STYLE="Baroque" → "elegant kittens in ornate royal garden"
ORIGINAL="random text", STYLE="Cubism" → "geometric abstract shapes and forms"
"""

# Image settings
IMAGE_SIZE = (256, 256)

# API Keys
# Get from https://console.groq.com/
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')

# constants.py
# Định nghĩa các hằng số và đường dẫn dùng chung cho project

DATA_BASE_DIR = 'kaggle/input'
WORKING_BASE_DIR = 'kaggle/working/art_styles'
LOG_DIR = 'app_log'
MODEL_FILENAME = 'art_style_classifier.h5'
TFLITE_MODEL_FILENAME = 'style_model.tflite'
LABELS_FILENAME = 'labels.txt'

STYLE_CLASSES = [
    'Baroque',
    'Expressionism',
    'Cubism',
    'Japanese_Art',
    'Art_Nouveau_Modern'
]

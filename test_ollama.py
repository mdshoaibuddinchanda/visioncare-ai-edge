import sys
import os

sys.path.append(r'c:\DR2\visioncare\visioncare-ai')
from services.ollama_service import OllamaService
from config.prompts import EYE_ANALYSIS_PROMPT
import base64

# Create a dummy image
img_path = r'c:\DR2\visioncare\visioncare-ai\test_img.jpg'
with open(img_path, 'wb') as f:
    f.write(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='))

srv = OllamaService()
res = srv.analyze_eye(img_path, EYE_ANALYSIS_PROMPT)
print('STATUS:', res['status'])
print('RESPONSE:', res['response'])
print('MESSAGE:', res['message'])

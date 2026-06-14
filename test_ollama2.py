import sys
import os

sys.path.append(r'c:\DR2\visioncare\visioncare-ai')
from services.ollama_service import OllamaService
from config.prompts import EYE_ANALYSIS_PROMPT
import base64

img_path = r'c:\DR2\visioncare\visioncare-ai\test_img.jpg'

srv = OllamaService()
# Temporary override to test without format="json"
import json
import urllib.request
def custom_analyze(image_path, prompt):
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("ascii")
    payload = {
        "model": "qwen2.5vl:3b",
        "prompt": prompt,
        "images": [image_data],
        "stream": False,
        "options": {
            "temperature": 0,
            "num_ctx": 4096,
            "num_predict": 1000,
        },
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "")
    except Exception as e:
        return f"ERROR: {e}"

print(custom_analyze(img_path, EYE_ANALYSIS_PROMPT))

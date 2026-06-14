"""
Local Ollama vision service for eye image analysis.
"""
import base64
import json
import urllib.error
import urllib.request

from config.settings import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaService:
    """Handles local vision requests through the Ollama HTTP API."""

    def __init__(self):
        self.base_url = OLLAMA_BASE_URL.rstrip("/")
        self.model = OLLAMA_MODEL

    def analyze_eye(self, image_path, prompt):
        """Analyze an image with the configured local vision model."""
        try:
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("ascii")

            payload = {
                "model": self.model,
                "prompt": prompt,
                "images": [image_data],
                "stream": False,
                "keep_alive": "10m",
                "options": {
                    "temperature": 0,
                    "num_ctx": 4096,
                    "num_predict": 1000,
                },
            }
            request = urllib.request.Request(
                f"{self.base_url}/api/generate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(request, timeout=300) as response:
                result = json.loads(response.read().decode("utf-8"))

            return {
                "status": "success",
                "response": result.get("response", ""),
                "message": "Local Ollama analysis completed successfully.",
            }
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            return {
                "status": "error",
                "response": "",
                "message": f"Ollama error: {exc}",
            }

    def generate_text(self, prompt, system_prompt=""):
        """Generate text response using Ollama API."""
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}"

            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "keep_alive": "10m",
                "options": {
                    "temperature": 0.3,
                    "num_ctx": 4096,
                },
            }
            request = urllib.request.Request(
                f"{self.base_url}/api/generate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(request, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))

            return {
                "status": "success",
                "response": result.get("response", ""),
            }
        except Exception as exc:
            return {
                "status": "error",
                "response": f"Error: {exc}",
            }

    def is_available(self):
        """Check that Ollama is running and the configured model is installed."""
        try:
            with urllib.request.urlopen(f"{self.base_url}/api/tags", timeout=3) as response:
                result = json.loads(response.read().decode("utf-8"))
            model_names = {model.get("name") for model in result.get("models", [])}
            return self.model in model_names
        except (OSError, urllib.error.URLError, json.JSONDecodeError):
            return False

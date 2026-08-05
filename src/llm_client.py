import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Set provider to 'ollama'
LLM_PROVIDER = "ollama"

class LLMClient:
    def __init__(self):
        # Ollama config
        self.ollama_url = os.getenv("OLLAMA_API_URL")
        self.ollama_model = "gemma4:latest"

    def query(self, prompt: str, system_prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.ollama_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 1.0,
            "stream": False
        }
        try:
            response = requests.post(self.ollama_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Ollama error: {e}")
            return ""

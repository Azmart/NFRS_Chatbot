# backend/llm_client.py

import requests

class LLMClient:
    def __init__(self, endpoint="http://localhost:1234/v1/completions", model="gemma:12b-instruct"):
        self.endpoint = endpoint
        self.model = model

    def generate_answer(self, prompt: str, max_tokens=512, temperature=0.2):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": None
        }

        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["text"].strip()
        except Exception as e:
            print(f"[ERROR] LLM generation failed: {e}")
            return "LLM Error."
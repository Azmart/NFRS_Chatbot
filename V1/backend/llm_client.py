# backend/llm_client.py

import requests

class LLMClient:
    def __init__(self, endpoint="http://localhost:1234/v1/chat/completions", model="gemma-3-12b-it"):
        self.endpoint = endpoint
        self.model = model

    def generate_answer(self, prompt: str, max_tokens=512, temperature=0.7):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Always cite sources at the end."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }

        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[ERROR] LLM chat call failed: {e}")
            return "Error: LLM response failed."
import os
import requests
from typing import Literal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class TranslationService:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in .env file. Please add it to your .env file.")
    
    def translate_to_english(self, text: str, source_lang: Literal["ne", "ne-roman"]) -> str:
        """Translate Nepali text (romanized or devanagari) to English using DeepSeek."""
        prompt = f"Translate the following {'romanized Nepali' if source_lang == 'ne-roman' else 'Nepali'} text to English. Only provide the translation, no explanations:\n\n{text}"
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Translation API error: {response.text}")
        
        return response.json()["choices"][0]["message"]["content"].strip()
    
    def translate_to_nepali(self, text: str, target_lang: Literal["ne", "ne-roman"]) -> str:
        """Translate English text to Nepali (romanized or devanagari) using DeepSeek."""
        script = "romanized Nepali" if target_lang == "ne-roman" else "Nepali (Devanagari script)"
        prompt = f"Translate the following English text to {script}. Only provide the translation, no explanations:\n\n{text}"
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Translation API error: {response.text}")
        
        return response.json()["choices"][0]["message"]["content"].strip() 
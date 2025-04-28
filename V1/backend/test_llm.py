# test_llm.py

from llm_client import LLMClient

client = LLMClient()
prompt = "What is NFRS?"
print("🧠 Sending prompt...")
response = client.generate_answer(prompt)
print("💬 Response:", response)
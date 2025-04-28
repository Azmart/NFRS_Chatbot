# backend/pdf_loader.py

import os
import fitz  # PyMuPDF
from typing import List, Dict

CHUNK_SIZE = 500  # Adjust chunk size based on your LLM's token limit

def load_pdfs_recursive(base_folder: str) -> List[Dict]:
    documents = []

    for root, _, files in os.walk(base_folder):
        for filename in files:
            if not filename.lower().endswith(".pdf"):
                continue

            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, base_folder)
            try:
                pdf = fitz.open(file_path)
                for page_number, page in enumerate(pdf):
                    text = page.get_text().strip()
                    if not text:
                        continue

                    for i in range(0, len(text), CHUNK_SIZE):
                        chunk = text[i:i + CHUNK_SIZE]
                        documents.append({
                            "content": chunk,
                            "metadata": {
                                "source": relative_path.replace("\\", "/"),
                                "page": page_number + 1
                            }
                        })
            except Exception as e:
                print(f"[ERROR] Failed to read {relative_path}: {e}")
    
    return documents
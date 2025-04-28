# backend/embedding.py

from transformers import AutoTokenizer, AutoModel
import torch

class E5Embedder:
    def __init__(self, model_name="intfloat/e5-base"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def embed_texts(self, texts):
        """Batch embed a list of texts."""
        batch_dict = self.tokenizer(
            texts, padding=True, truncation=True, return_tensors="pt"
        )
        batch_dict = {k: v.to(self.device) for k, v in batch_dict.items()}
        with torch.no_grad():
            outputs = self.model(**batch_dict)
            embeddings = outputs.last_hidden_state[:, 0]  # CLS token
            return embeddings.cpu().numpy()

    def embed_document_text(self, text):
        """Embed a single document chunk with prefix as recommended by E5."""
        return self.embed_texts([f"passage: {text}"])[0]

    def embed_query(self, query):
        """Embed a query with 'query:' prefix."""
        return self.embed_texts([f"query: {query}"])[0]
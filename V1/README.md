# 📘 NFRS / IFRS Financial Reporting Assistant

> Retrieval-Augmented Generation (RAG) application for answering questions based on Nepal Financial Reporting Standards (NFRS) and International Financial Reporting Standards (IFRS).

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

---

## ✨ Features

- 💡 Intelligent question answering using your local **Gemma 3 LLM**
- 🔍 Embedding + retrieval using `E5-base` and **ChromaDB**
- 🧾 Answers include **source citations** (document name + page)
- 🖥️ Simple UI via **Streamlit**
- 🛠️ Fully local, secure, and offline-compatible

---

## 📂 Project Structure

```
nfrs_ifrs_rag_app/
├── backend/
│   ├── main.py               # FastAPI backend
│   ├── pdf_loader.py         # PDF parsing and chunking
│   ├── embedding.py          # Embedding model (E5-base)
│   ├── vector_store.py       # ChromaDB handling
│   ├── llm_client.py         # LM Studio API client (Gemma)
│   ├── rag_pipeline.py       # RAG pipeline logic
│   ├── index_documents.py    # Index PDFs to vector DB
├── frontend/
│   └── app.py                # Streamlit interface
├── data/
│   ├── documents/            # Folder with your PDF files
│   └── chroma_db/            # Vector database files
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/nfrs-ifrs-rag-app.git
cd nfrs-ifrs-rag-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your PDF Documents

Organize your PDFs in folders inside `data/documents/`:

```
data/documents/
├── IAS/
├── IFRIC/
├── IFRS/
├── PracticeStatements/
├── SIC/
```

---

## 🚀 How to Run

### 1. Run LM Studio

- Load **Gemma 3 12B Instruct**
- Make sure it’s accessible at `http://localhost:1234`

### 2. Index All PDFs

```bash
python backend/index_documents.py
```

### 3. Start FastAPI Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start Streamlit Frontend

```bash
streamlit run frontend/app.py
```

---

## 💬 Example Query

> **Q:** "How much tax is applicable for SME with annual revenue of 5 million rupees and profit of 1.3M?"

> **A:** Based on NFRS Document XX, Section YYY, Article ZZZ:  
> Up to 500K - no tax,  
> 500K–1M - 5%,  
> 1M–1.3M - 8%,  
> plus 13% VAT.  

> **[Source: NFRS_2022.pdf - Page 5]**

---

## 🧠 Tech Stack

| Component     | Tool |
|---------------|------|
| Language Model | [Gemma 3 12B Instruct](https://ai.google.dev/gemma) via LM Studio |
| Embeddings     | [`intfloat/e5-base`](https://huggingface.co/intfloat/e5-base) |
| Vector Store   | [ChromaDB](https://www.trychroma.com/) |
| Backend API    | [FastAPI](https://fastapi.tiangolo.com/) |
| Frontend UI    | [Streamlit](https://streamlit.io/) |
| PDF Parsing    | [PyMuPDF](https://pymupdf.readthedocs.io/) |

---

## 📌 Future Features

- [ ] Nepali language support 🇳🇵
- [ ] Dynamic PDF upload and reindexing
- [ ] Admin dashboard (document viewer)
- [ ] Docker support

---

## 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.  
Let’s make financial knowledge accessible, one regulation at a time.
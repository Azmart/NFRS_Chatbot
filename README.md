# NFRS/IFRS Document Q&A Chatbot

A chatbot application that uses local LLM (via LM Studio) to answer questions about NFRS and IFRS documents.

## Features

- Document processing with automatic section and reference detection
- Local LLM integration via LM Studio
- Vector storage using ChromaDB
- FastAPI backend
- Simple web frontend
- Detailed citations in responses

## Prerequisites

- Python 3.8+
- LM Studio with a compatible model (tested with gemma-3-12b-it)
- Node.js (optional, for serving frontend)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nfrs-ifrs-chatbot.git
cd nfrs-ifrs-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Place your PDF documents in the `data/documents` directory

5. Process the documents:
```bash
cd backend
python document_processor.py
```

6. Start the backend server:
```bash
uvicorn app:app --reload
```

7. Open the frontend/index.html in your browser

## Configuration

1. LM Studio Settings:
   - Context Length: 4096
   - Temperature: 0.3
   - Top P: 0.95
   - Max Tokens: 500
   - Uncheck "Stream Response"

2. Make sure LM Studio is running and listening on port 1234

## Project Structure
nfrs-ifrs-chatbot/
├── backend/
│ ├── app.py
│ ├── document_processor.py
│ └── requirements.txt
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
├── data/
│ └── documents/
├── .gitignore
└── README.md

## Usage

1. Start LM Studio and load your preferred model
2. Start the backend server
3. Open the frontend in a web browser
4. Ask questions about NFRS/IFRS documents

## License

[Your chosen license]

## Contributing

[Your contribution guidelines]


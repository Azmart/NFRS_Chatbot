import chromadb
from typing import List
import os
import PyPDF2
import re

def clean_metadata_value(value) -> str:
    """Convert None values to empty strings and ensure other values are strings."""
    if value is None:
        return ""
    return str(value)

def get_all_documents(root_dir: str) -> List[str]:
    """
    Recursively get all PDF documents from the root directory and its subdirectories.
    """
    document_paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.pdf'):
                full_path = os.path.join(dirpath, filename)
                document_paths.append(full_path)
    return document_paths

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:  # Open in binary mode
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from each page
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
                
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {str(e)}")
        raise
        
    return text

def extract_section_info(text: str) -> dict:
    """
    Extract section numbers, points, and other structural information from the text.
    """
    # Example patterns - adjust these based on your actual document structure
    section_pattern = r'Section\s+(\d+\.?\d*)'
    point_pattern = r'Point\s+(\d+\.?\d*)'
    article_pattern = r'Article\s+(\d+\.?\d*)'
    paragraph_pattern = r'Paragraph\s+(\d+\.?\d*)'
    
    section_match = re.search(section_pattern, text, re.IGNORECASE)
    point_match = re.search(point_pattern, text, re.IGNORECASE)
    article_match = re.search(article_pattern, text, re.IGNORECASE)
    paragraph_match = re.search(paragraph_pattern, text, re.IGNORECASE)
    
    return {
        "section": clean_metadata_value(section_match.group(1) if section_match else None),
        "point": clean_metadata_value(point_match.group(1) if point_match else None),
        "article": clean_metadata_value(article_match.group(1) if article_match else None),
        "paragraph": clean_metadata_value(paragraph_match.group(1) if paragraph_match else None)
    }

def process_document(file_path: str, collection, chunk_size: int = 1000):
    """
    Process a single document and store its chunks in ChromaDB with enhanced metadata.
    """
    try:
        text = extract_text_from_pdf(file_path)
        relative_path = os.path.relpath(file_path, start='./data/documents')
        document_name = os.path.basename(file_path)
        
        # Split into paragraphs instead of fixed-size chunks
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        
        for i, paragraph in enumerate(paragraphs):
            # Extract structural information
            section_info = extract_section_info(paragraph)
            
            # Create detailed metadata with cleaned values
            metadata = {
                "source": clean_metadata_value(relative_path),
                "document_name": clean_metadata_value(document_name),
                "chunk_id": str(i),  # Convert to string to ensure consistency
                "section": section_info["section"],
                "point": section_info["point"],
                "article": section_info["article"],
                "paragraph": section_info["paragraph"],
                "full_path": clean_metadata_value(file_path),
                "text_type": "NFRS" if "NFRS" in file_path else "IFRS"
            }
            
            # Additional document type detection
            if "SIC" in file_path:
                metadata["document_type"] = "SIC"
            elif "IFRIC" in file_path:
                metadata["document_type"] = "IFRIC"
            else:
                metadata["document_type"] = "Standard"
            
            collection.add(
                documents=[paragraph],
                metadatas=[metadata],
                ids=[f"{relative_path}_para_{i}"]
            )
            
        print(f"Successfully processed: {relative_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def process_all_documents(documents_dir: str = "./data/documents", chunk_size: int = 1000):
    """
    Process all documents in the directory and its subdirectories.
    """
    try:
        # Initialize ChromaDB
        chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
        
        # Get or create collection
        collection = chroma_client.get_or_create_collection(name="document_qa")
        
        # Get all document paths
        document_paths = get_all_documents(documents_dir)
        
        if not document_paths:
            print("No PDF documents found in the specified directory!")
            return
        
        print(f"Found {len(document_paths)} PDF documents to process.")
        
        # Process each document
        for doc_path in document_paths:
            print(f"Processing: {doc_path}")
            process_document(doc_path, collection, chunk_size)
            
    except Exception as e:
        print(f"Error during document processing: {str(e)}")
        raise

if __name__ == "__main__":
    # Make sure the data directory exists
    os.makedirs("./data/chroma_db", exist_ok=True)
    
    # Process all documents
    try:
        process_all_documents()
        print("Document processing completed successfully!")
    except Exception as e:
        print(f"Failed to complete document processing: {str(e)}")

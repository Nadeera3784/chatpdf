import os
import uuid
from typing import List, Dict, Any
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from services.pinecone_service import PineconeService

class PDFService:
    def __init__(self):
        self.pinecone_service = PineconeService()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        try:
            text_chunks = []
            
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    
                    if page_text and page_text.strip():
                        chunks = self.text_splitter.split_text(page_text)
                        
                        for chunk in chunks:
                            if chunk.strip(): 
                                text_chunks.append({
                                    'text': chunk.strip(),
                                    'page_number': page_num,
                                    'source': os.path.basename(pdf_path)
                                })
            
            return text_chunks
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {e}")
    
    def process_pdf(self, pdf_file, filename: str) -> Dict[str, Any]:
        try:
            pdf_id = str(uuid.uuid4())
            
            upload_dir = "/backend/data"
            os.makedirs(upload_dir, exist_ok=True)
            
            pdf_path = os.path.join(upload_dir, f"{pdf_id}_{filename}")
            pdf_file.save(pdf_path)
            
            text_chunks = self.extract_text_from_pdf(pdf_path)
            
            if not text_chunks:
                raise ValueError("No text could be extracted from the PDF")
            
            self.pinecone_service.store_pdf_chunks(pdf_id, text_chunks)
            
            # os.remove(pdf_path)
            
            return {
                'pdf_id': pdf_id,
                'filename': filename,
                'total_chunks': len(text_chunks),
                'total_pages': max([chunk['page_number'] for chunk in text_chunks]) if text_chunks else 0,
                'status': 'processed'
            }
            
        except Exception as e:
            raise ValueError(f"Failed to process PDF: {e}")
    
    def get_pdf_info(self, pdf_id: str) -> Dict[str, Any]:
        try:
            return {
                'pdf_id': pdf_id,
                'status': 'ready',
                'message': 'PDF is ready for chat'
            }
            
        except Exception as e:
            raise ValueError(f"Failed to get PDF info: {e}")
    
    def delete_pdf(self, pdf_id: str):
        try:
            self.pinecone_service.delete_pdf_data(pdf_id)
            return {'status': 'deleted', 'pdf_id': pdf_id}
            
        except Exception as e:
            raise ValueError(f"Failed to delete PDF: {e}")

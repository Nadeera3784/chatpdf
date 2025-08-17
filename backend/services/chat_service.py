from typing import List, Dict, Any
from openai import OpenAI
from services.pinecone_service import PineconeService
from configuration.configuration import Configuration

class ChatService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=Configuration.OPENAI_API_KEY)
        self.pinecone_service = PineconeService()
    
    def chat_with_pdf(self, query: str, pdf_id: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        try:
            if chat_history is None:
                chat_history = []
            
            similar_chunks = self.pinecone_service.search_similar_chunks(
                query=query, 
                pdf_id=pdf_id, 
                top_k=5
            )
            
            if not similar_chunks:
                return {
                    'response': "I couldn't find relevant information in the PDF to answer your question.",
                    'sources': []
                }
            
            context = "\n\n".join([
                f"Page {chunk['page_number']}: {chunk['text']}" 
                for chunk in similar_chunks
            ])

            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful AI assistant that answers questions based on the provided PDF content. 
                    Use only the information from the PDF context to answer questions. 
                    If the answer is not in the provided context, say so clearly.
                    Be concise and accurate in your responses.
                    Always reference the page numbers when possible."""
                }
            ]
            
            for msg in chat_history[-10:]: 
                messages.append(msg)
            
            messages.append({
                "role": "user",
                "content": f"""Based on the following PDF content, please answer this question: {query}

PDF Content:
{context}

Question: {query}"""
            })
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.1
            )
            
            answer = response.choices[0].message.content

            sources = [
                {
                    'page_number': chunk['page_number'],
                    'preview': chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'],
                    'relevance_score': round(chunk['score'], 3)
                }
                for chunk in similar_chunks
            ]
            
            return {
                'response': answer,
                'sources': sources,
                'query': query
            }
            
        except Exception as e:
            return {
                'response': f"An error occurred while processing your question: {str(e)}",
                'sources': []
            }
    
    def get_pdf_summary(self, pdf_id: str) -> str:
        try:
            sample_chunks = self.pinecone_service.search_similar_chunks(
                query="summary overview main points", 
                pdf_id=pdf_id, 
                top_k=10
            )
            
            if not sample_chunks:
                return "No content found for this PDF."
            
            context = "\n\n".join([chunk['text'] for chunk in sample_chunks])
            
            # Generate summary
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that creates concise summaries of PDF content."
                },
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following PDF content:\n\n{context}"
                }
            ]
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"

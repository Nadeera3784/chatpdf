import os
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from configuration.configuration import Configuration

class PineconeService:
    def __init__(self):
        self.pc = Pinecone(api_key=Configuration.PINECONE_API_KEY)
        self.openai_client = OpenAI(api_key=Configuration.OPENAI_API_KEY)
        self.index_name = Configuration.PINECONE_INDEX_NAME
        self.dimension = Configuration.PINECONE_VECTOR_DIMENSION  
        self.pinecone_index_region = Configuration.PINECONE_INDEX_REGION
        self.pinecone_index_cloud = Configuration.PINECONE_INDEX_CLOUD

        self._initialize_index()
    
    def _initialize_index(self):
        try:
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud=self.pinecone_index_cloud,
                        region=self.pinecone_index_region
                    )
                )
            
            self.index = self.pc.Index(self.index_name)
            
        except Exception as e:
            raise ValueError(f"Failed to initialize Pinecone index: {e}")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            model = "text-embedding-ada-002"
            
            response = self.openai_client.embeddings.create(
                model=model,
                input=texts
            )
            
            return [item.embedding for item in response.data]
            
        except Exception as e:
            raise ValueError(f"Failed to generate embeddings: {e}")
    
    def store_pdf_chunks(self, pdf_id: str, chunks: List[Dict[str, Any]]):
        try:
            texts = [chunk['text'] for chunk in chunks]
            embeddings = self.generate_embeddings(texts)
            
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                vector_id = f"{pdf_id}_chunk_{i}"
                metadata = {
                    'pdf_id': pdf_id,
                    'chunk_index': i,
                    'text': chunk['text'],
                    'page_number': chunk.get('page_number', 0)
                }
                vectors.append({
                    'id': vector_id,
                    'values': embedding,
                    'metadata': metadata
                })
            
            self.index.upsert(vectors=vectors)
            
        except Exception as e:
            raise ValueError(f"Failed to store PDF chunks: {e}")
    
    def search_similar_chunks(self, query: str, pdf_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        try:
            query_embedding = self.generate_embeddings([query])[0]
            
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter={'pdf_id': pdf_id}
            )
            
            similar_chunks = []
            for match in results.matches:
                similar_chunks.append({
                    'text': match.metadata['text'],
                    'page_number': match.metadata['page_number'],
                    'score': match.score,
                    'chunk_index': match.metadata['chunk_index']
                })
            
            return similar_chunks
            
        except Exception as e:
            raise ValueError(f"Failed to search similar chunks: {e}")
    
    def delete_pdf_data(self, pdf_id: str):
        try:
            results = self.index.query(
                vector=[0] * self.dimension,  
                top_k=10000,  # get all
                include_metadata=True,
                filter={'pdf_id': pdf_id}
            )
            
            if results.matches:
                vector_ids = [match.id for match in results.matches]
                self.index.delete(ids=vector_ids)
                
        except Exception as e:
            raise ValueError(f"Failed to delete PDF data: {e}")

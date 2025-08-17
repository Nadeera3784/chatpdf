import os
from dotenv import load_dotenv

load_dotenv()

class Configuration:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "chatpdf-index")
    PINECONE_INDEX_REGION = os.getenv("PINECONE_INDEX_REGION", "us-east-1")
    PINECONE_VECTOR_DIMENSION = int(os.getenv("PINECONE_VECTOR_DIMENSION", 1536))
    PINECONE_INDEX_CLOUD = os.getenv("PINECONE_INDEX_CLOUD", "aws")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./data")
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not cls.PINECONE_API_KEY:
            missing.append("PINECONE_API_KEY")
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

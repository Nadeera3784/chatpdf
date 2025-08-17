# ChatPDF - LLM-Powered Document Conversation System

I created this project to explore how Large Language Models (LLMs) work with custom data feeds. My goal was to understand the complete pipeline of document processing, from chunking and embedding to storing in vector databases and querying with LLMs.

This ChatPDF application demonstrates the full Retrieval-Augmented Generation (RAG) workflow using real-world technologies like OpenAI's GPT models, Pinecone vector database, and modern web frameworks.

## What I Built

A complete document conversation system that allows users to:
- Upload PDF documents 
- Have intelligent conversations with the content
- Get AI-generated summaries
- See source references for AI responses

## The Technical Journey

### 1. Document Processing Pipeline
I implemented a robust PDF processing system using `pdfplumber` that:
- Extracts text from PDF pages
- Uses LangChain's text splitters to create optimal chunks
- Preserves page references for source attribution

### 2. Embedding & Vector Storage
The system converts text chunks into vector embeddings:
- Uses OpenAI's `text-embedding-ada-002` model (1536 dimensions)
- Stores embeddings in Pinecone vector database
- Implements semantic search for relevant content retrieval

### 3. LLM Integration
For intelligent responses, I integrated:
- OpenAI's GPT-3.5-turbo for chat completions
- Context-aware conversations with chat history
- Source-grounded responses to prevent hallucination

### 4. Modern Web Architecture
Built with production-ready technologies:
- **Backend**: Flask REST API with Docker containerization
- **Frontend**: React with TypeScript and Tailwind CSS

## Architecture Overview

```
PDF Upload → Text Extraction → Chunking → Embedding → Pinecone Storage
                                                            ↓
User Query → Embedding → Similarity Search → Context Retrieval → LLM Response
```

## Key Features

### 🔄 **Complete RAG Pipeline**
- Document ingestion and preprocessing
- Vector embeddings with semantic search
- Context-aware LLM responses

### 📊 **Smart Chunking**
- Recursive text splitting with overlap
- Page number preservation
- Optimal chunk sizes for embeddings

### 🎯 **Accurate Responses**
- Source attribution with page references
- Relevance scoring for retrieved content
- Context-limited responses to prevent hallucination


## Technology Stack

### Backend
- **Python 3.12** - Core language
- **Flask** - REST API framework
- **OpenAI API** - LLM and embeddings
- **Pinecone** - Vector database
- **pdfplumber** - PDF text extraction
- **LangChain** - Text processing utilities

### Frontend
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Vite** - Build tool

### Infrastructure
- **Docker** - Containerization
- **CORS** - Cross-origin support



Through building this project, I gained deep insights into:

How text is converted to numerical representations and why dimension matching is crucial
How similarity search works in high-dimensional spaces
The complete pipeline from document ingestion to contextual responses
How to provide context to language models for accurate, grounded responses
Error handling and deployment practices

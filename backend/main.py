from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from configuration.configuration import Configuration
from services.pdf_service import PDFService
from services.chat_service import ChatService

app = Flask(__name__)
CORS(app) 

UPLOAD_FOLDER = '/backend/data'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 


pdf_service = PDFService()
chat_service = ChatService()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    return {"message": "ChatPDF Backend API", "status": "running"}

@app.route("/health", methods=["GET"])
def health_check():
    try:
        Configuration.validate()
        return {"status": "healthy", "message": "All services are running"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500



@app.route("/upload", methods=["POST"])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return {"error": "No file provided"}, 400
        
        file = request.files['file']
        
        if file.filename == '':
            return {"error": "No file selected"}, 400
        
        if not (file and allowed_file(file.filename)):
            return {"error": "Only PDF files are allowed"}, 400
        
        filename = secure_filename(file.filename)
        
        result = pdf_service.process_pdf(file, filename)
        
        return {
            "success": True,
            "message": "PDF processed successfully",
            "data": result
        }
        
    except Exception as e:
        return {"error": f"Failed to process PDF: {str(e)}"}, 500

@app.route("/chat", methods=["POST"])
def chat_with_pdf():
    try:
        data = request.get_json()
        
        if not data:
            return {"error": "No data provided"}, 400
        
        pdf_id = data.get('pdf_id')
        query = data.get('query')
        chat_history = data.get('chat_history', [])
        
        if not pdf_id:
            return {"error": "PDF ID is required"}, 400
        
        if not query:
            return {"error": "Query is required"}, 400
        
        result = chat_service.chat_with_pdf(query, pdf_id, chat_history)
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        return {"error": f"Chat failed: {str(e)}"}, 500

@app.route("/pdf/<pdf_id>/summary", methods=["GET"])
def get_pdf_summary(pdf_id):
    try:
        summary = chat_service.get_pdf_summary(pdf_id)
        
        return {
            "success": True,
            "data": {
                "pdf_id": pdf_id,
                "summary": summary
            }
        }
        
    except Exception as e:
        return {"error": f"Failed to get summary: {str(e)}"}, 500

@app.route("/pdf/<pdf_id>", methods=["GET"])
def get_pdf_info(pdf_id):
    try:
        info = pdf_service.get_pdf_info(pdf_id)
        
        return {
            "success": True,
            "data": info
        }
        
    except Exception as e:
        return {"error": f"Failed to get PDF info: {str(e)}"}, 500

@app.route("/pdf/<pdf_id>", methods=["DELETE"])
def delete_pdf(pdf_id):
    try:
        result = pdf_service.delete_pdf(pdf_id)
        
        return {
            "success": True,
            "message": "PDF deleted successfully",
            "data": result
        }
        
    except Exception as e:
        return {"error": f"Failed to delete PDF: {str(e)}"}, 500

if __name__ == "__main__":
    try:
        Configuration.validate()
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        app.run(host="0.0.0.0", port=8080, debug=False)
        
    except Exception as e:
        print(f"Failed to start server: {e}")
        exit(1)
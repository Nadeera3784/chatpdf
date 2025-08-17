import { useState } from 'react';
import Header from "./Header";
import Footer from "./Footer";
import PDFUpload from "./PDFUpload";
import ChatInterface from "./ChatInterface";

interface PDFData {
  pdf_id: string;
  filename: string;
  total_chunks: number;
  total_pages: number;
  status: string;
}

function Application() {
  const [currentPDF, setCurrentPDF] = useState<PDFData | null>(null);

  const handleUploadSuccess = (pdfData: PDFData) => {
    setCurrentPDF(pdfData);
  };

  const handleBackToUpload = () => {
    setCurrentPDF(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="flex-1">
        {!currentPDF ? (
          <div className="container mx-auto py-8">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-800 mb-4">
                Chat with Your PDF
              </h1>
              <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                Upload a PDF document and start asking questions. Our AI will help you find information quickly and accurately.
              </p>
            </div>
            <PDFUpload onUploadSuccess={handleUploadSuccess} />
          </div>
        ) : (
          <ChatInterface pdfData={currentPDF} onBack={handleBackToUpload} />
        )}
      </main>
      
      {!currentPDF && <Footer />}
    </div>
  );
}

export default Application;

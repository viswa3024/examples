'use client';
import { useState } from 'react';
import ChatPanel from './components/ChatPanel';
import PdfPreview from './components/PdfPreview';

export default function HomePage() {
  const [pdfUrl, setPdfUrl] = useState('');

  const handlePdfClick = (url: string) => setPdfUrl(url);
  const handlePdfClose = () => setPdfUrl('');

  return (
    <div className="w-full h-screen flex flex-col">
      {/* Fixed header */}
      <div className="h-[35px] bg-blue-600 text-white px-4 flex items-center text-sm font-medium shadow-sm">
        Chatbot
      </div>

      {/* Main chat/pdf content */}
      <div className="flex flex-1 w-full overflow-hidden" style={{ height: 'calc(100vh - 35px)' }}>
        {/* Chat Panel */}
        <div className={`transition-all duration-300 ${pdfUrl ? 'w-full md:w-1/2' : 'w-full'}`}>
          <ChatPanel onPdfClick={handlePdfClick} />
        </div>

        {/* Conditional PDF Panel */}
        {pdfUrl && (
          <div className="hidden md:block w-1/2 border-l border-gray-300 bg-gray-50">
            <PdfPreview pdfUrl={pdfUrl} onClose={handlePdfClose} />
          </div>
        )}
      </div>
    </div>
  );
}

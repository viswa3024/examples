'use client';
import { useState } from 'react';
import ChatPanel from './components/ChatPanel';
import PdfPreview from './components/PdfPreview';

export default function HomePage() {
  const [pdfUrl, setPdfUrl] = useState('');

  const handlePdfClick = (url: string) => setPdfUrl(url);
  const handlePdfClose = () => setPdfUrl('');

  return (
    <div className="flex flex-col h-screen w-full overflow-hidden">
      {/* Fixed header (35px height) */}
      <header className="h-[35px] bg-white border-b px-4 flex items-center shadow-sm">
        <h1 className="text-sm font-medium">Chatbot</h1>
      </header>

      {/* Main content area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Chat panel - full width by default, shrinks when PDF open */}
        <div className={`transition-all duration-300 h-full ${pdfUrl ? 'w-full md:w-1/2' : 'w-full'}`}>
          <ChatPanel onPdfClick={handlePdfClick} />
        </div>

        {/* PDF preview panel - shown only when pdfUrl is set */}
        {pdfUrl && (
          <div className="hidden md:block w-1/2 h-full border-l border-gray-300 bg-gray-50">
            <PdfPreview pdfUrl={pdfUrl} onClose={handlePdfClose} />
          </div>
        )}
      </div>
    </div>
  );
}

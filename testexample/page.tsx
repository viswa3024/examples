'use client';
import { useState } from 'react';
import ChatPanel from './components/ChatPanel';
import PdfPreview from './components/PdfPreview';

export default function HomePage() {
  const [pdfUrl, setPdfUrl] = useState('');

  const handlePdfClick = (url: string) => {
    setPdfUrl(url); // triggers right section
  };

  const handlePdfClose = () => {
    setPdfUrl(''); // hides right section
  };

  return (
    <div className="flex h-screen w-full overflow-hidden">
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
  );
}






// 'use client';

// import { useRef, useState } from 'react';
// import { renderAsync, Options } from 'docx-preview';

// export default function Home() {
//   const containerRef = useRef<HTMLDivElement | null>(null);
//   const [error, setError] = useState<string | null>(null);

//   const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
//     const file = e.target.files?.[0];
//     if (!file || !file.name.endsWith('.docx')) {
//       alert('Please upload a valid .docx file');
//       return;
//     }

//     try {
//       const arrayBuffer = await file.arrayBuffer();

//       if (containerRef.current) {
//         containerRef.current.innerHTML = '';

//         const options: Partial<Options> = {
//           className: 'docx-preview',
//           ignoreWidth: false,
//           ignoreHeight: false,
//           ignoreFonts: false,
//           breakPages: true,
//           inWrapper: true,
//           trimXmlDeclaration: true,
//           useBase64URL: false,
//         };

//         await renderAsync(arrayBuffer, containerRef.current, options);
//       }
//     } catch (err) {
//       console.error(err);
//       setError('❌ Failed to render document.');
//     }
//   };

//   return (
//     <main className="p-6 max-w-5xl mx-auto">
//       <h1 className="text-2xl font-bold mb-6">📄 DOCX Preview (docx-preview)</h1>

//       <input
//         type="file"
//         accept=".docx"
//         onChange={handleUpload}
//         className="mb-6 border p-2 rounded"
//       />

//       {error && <p className="text-red-500 mb-4">{error}</p>}

//       <div
//         ref={containerRef}
//         className="border p-4 bg-white rounded shadow overflow-auto max-h-[80vh]"
//       />
//     </main>
//   );
// }

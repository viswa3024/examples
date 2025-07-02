'use client';

export default function PdfPreview({ pdfUrl, onClose }: { pdfUrl: string; onClose: () => void }) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex justify-between items-center p-3 bg-white border-b">
        <h2 className="text-lg font-semibold">Generated Document</h2>
        <div className="flex gap-2">
          <a href={pdfUrl} download className="btn btn-sm btn-success">Download</a>
          <button onClick={onClose} className="btn btn-sm btn-outline-danger">Close</button>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        <iframe
          src={pdfUrl}
          className="w-full h-full"
          style={{ border: 'none' }}
        />
      </div>
    </div>
  );
}

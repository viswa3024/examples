import { useState } from 'react';

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const YourComponent = () => {
  const [handleGenerateLoading, setHandleGenerateLoading] = useState(false);

  const handleGenerate = async () => {
    try {
      setHandleGenerateLoading(true);

      // Simulate delay
      await sleep(60000); // 60,000 ms = 60 seconds

      // Call your API route (example)
      const res = await fetch('/api/docx');
      if (!res.ok) throw new Error('Failed to fetch document');

      const blob = await res.blob();

      const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, ''); // YYYYMMDD
      const filename = `demo-${timestamp}.docx`;

      // Trigger download using file-saver
      const fileURL = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = fileURL;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(fileURL);
    } catch (err) {
      console.error('Error during generation:', err);
    } finally {
      setHandleGenerateLoading(false);
    }
  };

  return (
    <button
      onClick={handleGenerate}
      disabled={handleGenerateLoading}
      className="bg-blue-500 text-white px-4 py-2 rounded"
    >
      {handleGenerateLoading ? 'Generating...' : 'Generate and Download'}
    </button>
  );
};










//===============================================================

import { useState } from 'react';

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const YourComponent = () => {
  const [handleGenerateLoading, setHandleGenerateLoading] = useState(false);

  const handleGenerate = async () => {
    try {
      setHandleGenerateLoading(true);

      // Wait for 60 seconds
      await sleep(60000);

      // 👇 API logic will be added later
    } catch (err) {
      console.error('Error during generation:', err);
    } finally {
      setHandleGenerateLoading(false);
    }
  };

  return (
    <button
      onClick={handleGenerate}
      disabled={handleGenerateLoading}
      className="bg-blue-500 text-white px-4 py-2 rounded"
    >
      {handleGenerateLoading ? 'Generating...' : 'Generate and Download'}
    </button>
  );
};


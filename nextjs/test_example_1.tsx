import { useState } from 'react';

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const YourComponent = () => {
  const [handleGenerateLoading, setHandleGenerateLoading] = useState(false);
  const [documentGenerated, setDocumentGenerated] = useState(false);
  const [error, setError] = useState<string | null>(null); // 👈 For error messages

  const handleGenerate = async () => {
    try {
      setHandleGenerateLoading(true);
      setError(null); // Clear previous error

      // Simulate 60-second generation delay
      await sleep(60000);

      // 🔥 Simulate error
      throw new Error('Something went wrong while generating the document');

      // Set flag if no error occurs (won’t reach here because of the throw)
      setDocumentGenerated(true);
    } catch (err: any) {
      console.error('Error during generation:', err);
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setHandleGenerateLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <button
        onClick={handleGenerate}
        disabled={handleGenerateLoading}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {handleGenerateLoading ? 'Generating...' : 'Generate Document'}
      </button>

      {error && (
        <p className="text-red-600 font-medium">
          ❌ {error}
        </p>
      )}

      {documentGenerated && !error && (
        <p className="text-green-600 font-medium">
          ✅ Document is ready to download!
        </p>
      )}
    </div>
  );
};

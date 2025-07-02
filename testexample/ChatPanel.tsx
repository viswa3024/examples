'use client';

import { useEffect, useRef, useState } from 'react';

export default function ChatPanel({ onPdfClick }: { onPdfClick: (url: string) => void }) {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Welcome to Chat bot' },
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    const botMsg = {
      sender: 'bot',
      text: 'Click the link below to preview/download the generated document.',
      file: '/sample.pdf',
    };

    setMessages((prev) => [...prev, userMsg, botMsg]);
    setInput('');
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="h-full bg-white flex flex-col">
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg: any, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-md max-w-[85%] ${
              msg.sender === 'bot'
                ? 'bg-blue-100 text-left'
                : 'bg-green-100 text-right ml-auto'
            }`}
          >
            <p>{msg.text}</p>
            {msg.sender === 'bot' && msg.file && (
              <button
                onClick={() => onPdfClick(msg.file!)}
                className="mt-2 text-blue-600 underline hover:text-blue-800"
              >
                📥 v1.pdf
              </button>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input section */}
      <div className="border-t bg-white p-3">
        <div className="relative">
          <textarea
            rows={2}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Provide your document brief here."
            className="w-full border border-gray-300 rounded-lg py-3 pr-12 pl-4 resize-none focus:outline-none focus:ring-2 focus:ring-blue-300"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button
            onClick={handleSend}
            className="absolute bottom-3 right-4 text-gray-500 hover:text-blue-500"
          >
            {/* Send icon */}
            <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

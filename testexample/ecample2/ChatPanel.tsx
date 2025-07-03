'use client';

import { useEffect, useRef, useState } from 'react';

export default function ChatPanel({ onPdfClick }: { onPdfClick: (url: string) => void }) {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Welcome to Chat bot' },
  ]);
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [showScrollButton, setShowScrollButton] = useState(false);
  const [textareaHeight, setTextareaHeight] = useState(48);


  // const handleSend = () => {
  //   if (!input.trim()) return;

  //   const userMsg = { sender: 'user', text: input };
  //   const botMsg = {
  //     sender: 'bot',
  //     text: 'Click the link below to preview/download the generated document.',
  //     file: '/sample.pdf',
  //   };

  //   setMessages((prev) => [...prev, userMsg, botMsg]);
  //   setInput('');
  // };

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
  
  // 💡 Reset height on clear
  if (textareaRef.current) {
    textareaRef.current.style.height = 'auto';
     setTextareaHeight(48);
  }
};


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
  const container = messagesContainerRef.current;
  if (!container) return;

  const handleScroll = () => {
    const isAtBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight < 50;
    setShowScrollButton(!isAtBottom);
  };

  container.addEventListener('scroll', handleScroll);
  return () => container.removeEventListener('scroll', handleScroll);
}, []);

//   const adjustTextareaHeight = () => {
//   const el = textareaRef.current;
//   if (el) {
//     el.style.height = 'auto'; // reset first
//     el.style.height = Math.min(el.scrollHeight, 160) + 'px'; // 5 rows max
//   }
// };

const adjustTextareaHeight = () => {
  const el = textareaRef.current;
  if (el) {
    el.style.height = 'auto';
    const newHeight = Math.min(el.scrollHeight, 160); // max 5 rows
    el.style.height = newHeight + 'px';
    setTextareaHeight(newHeight);
  }
};
  return (
    <div className="h-full bg-white flex flex-col">
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4" ref={messagesContainerRef}>
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

        {/* {showScrollButton && (
    <button
      onClick={scrollToBottom}
      className="absolute bottom-4 right-4 bg-blue-600 text-white rounded-full p-2 shadow hover:bg-blue-700"
      title="Scroll to latest"
    >
      ⬇️
    </button>
  )} */}

  {/* {showScrollButton && (
  <button
    onClick={scrollToBottom}
    className="absolute bottom-3 left-1/2 -translate-x-1/2 bg-white text-black rounded-full shadow-md w-8 h-8 flex items-center justify-center border border-gray-300 hover:shadow-lg transition-all"
    title="Scroll to latest"
  >
    <span className="text-xl leading-none">↓</span>
  </button>
)} */}

 {/* {showScrollButton && (
    <button
      onClick={scrollToBottom}
      className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-white text-black rounded-full shadow-md w-8 h-8 flex items-center justify-center border border-gray-300 hover:shadow-lg transition-all z-10"
      title="Scroll to latest"
    >
      <span className="text-xl leading-none">↓</span>
    </button>
  )} */}

   {/* {showScrollButton && (
    <button
      onClick={scrollToBottom}
      className="fixed bottom-[80px] left-1/2 -translate-x-1/2 bg-white text-black rounded-full shadow-md w-8 h-8 flex items-center justify-center border border-gray-300 hover:shadow-lg z-50"
      title="Scroll to latest"
    >
      <span className="text-xl leading-none">↓</span>
    </button>
  )} */}
      </div>

      {/* {showScrollButton && (
    <div className="absolute bottom-[72px] left-1/2 -translate-x-1/2 z-20">
      <button
        onClick={scrollToBottom}
        className="bg-white text-black rounded-full shadow-md w-8 h-8 flex items-center justify-center border border-gray-300 hover:shadow-lg"
        title="Scroll to latest"
      >
        <span className="text-xl leading-none">↓</span>
      </button>
    </div>
  )} */}

  {showScrollButton && (
  <div
    className="absolute left-1/2 -translate-x-1/2 z-20"
    style={{ bottom: textareaHeight + 40 }} // 24px margin above textarea
  >
    <button
      onClick={scrollToBottom}
      className="w-10 h-10 bg-white rounded-full text-black  shadow-md w-8 h-8 flex items-center justify-center border border-gray-300 hover:shadow-lg"
      style={{ borderRadius: '50%' }}
      title="Scroll to latest"
    >
      {/* <span className="text-xl leading-none"> ↓ </span> */}
        
       {/* <span className="text-xl leading-none">

        <svg xmlns="http://www.w3.org/2000/svg"
     fill="none"
     viewBox="0 0 24 24"
     strokeWidth={2}
     stroke="currentColor"
     className="w-5 h-5">
  <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
</svg>
        
        
        </span> */}

         <svg
    width="20"
    height="20"
    viewBox="0 0 20 20"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    className="text-gray-700"
  >
    <path d="M9.33468 3.33333C9.33468 2.96617 9.6326 2.66847 9.99972 2.66829C10.367 2.66829 10.6648 2.96606 10.6648 3.33333V15.0609L15.363 10.3626L15.4675 10.2777C15.7255 10.1074 16.0762 10.1357 16.3034 10.3626C16.5631 10.6223 16.5631 11.0443 16.3034 11.304L10.4704 17.137C10.2108 17.3967 9.7897 17.3966 9.52999 17.137L3.69601 11.304L3.61105 11.1995C3.44054 10.9414 3.46874 10.5899 3.69601 10.3626C3.92328 10.1354 4.27479 10.1072 4.53292 10.2777L4.63741 10.3626L9.33468 15.0599V3.33333Z"></path>
  </svg>
    </button>
  </div>
)}

      {/* Input section */}
      <div className="border-t bg-white p-3">
        <div className="relative">
          {/* <textarea
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
          /> */}

          {/* <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Provide your document brief here."
            className="w-full max-h-[160px] min-h-[48px] overflow-y-auto border border-gray-300 rounded-lg py-3 pr-12 pl-4 resize-none focus:outline-none focus:ring-2 focus:ring-blue-300"
            style={{ height: 'auto' }}
            rows={1}
            onInput={(e) => {
              const target = e.target as HTMLTextAreaElement;
              target.style.height = 'auto'; // reset
              target.style.height = Math.min(target.scrollHeight, 160) + 'px'; // max 160px = ~5 rows
            }}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          /> */}

          <textarea
  ref={textareaRef}
  value={input}
  onChange={(e) => {
    setInput(e.target.value);
    adjustTextareaHeight();
  }}
  placeholder="Provide your document brief here."
  className="w-full max-h-[160px] min-h-[48px] overflow-y-auto border border-gray-300 rounded-lg py-3 pr-12 pl-4 resize-none focus:outline-none focus:ring-2 focus:ring-blue-300"
  style={{ height: 'auto' }}
  rows={1}
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

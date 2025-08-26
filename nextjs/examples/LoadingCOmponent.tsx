"use client";

import { useEffect, useState } from "react";

interface LoadingComponentProps {
  forceComplete?: boolean; // parent sets true when API finishes
}

export default function LoadingComponent({ forceComplete }: LoadingComponentProps) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (forceComplete) {
      setProgress(100); // jump instantly when API done
      return;
    }

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev < 40) {
          // ⚡ fast growth phase
          return Math.min(prev + Math.random() * 15 + 10, 40);
        } else if (prev < 90) {
          // steady phase
          return Math.min(prev + Math.random() * 3 + 1, 90);
        } else if (prev < 99) {
          // crawling phase
          return Math.min(prev + Math.random() * 0.5 + 0.2, 99);
        }
        return prev;
      });
    }, 300); // tick every 300ms

    return () => clearInterval(interval);
  }, [forceComplete]);

  return (
    <div className="flex flex-col items-center justify-center gap-4 p-6 bg-white rounded-2xl shadow-lg w-80">
      <p className="text-gray-700 font-medium">Generating Document...</p>
      <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
        <div
          className="bg-blue-600 h-4 transition-all duration-300 ease-in-out"
          style={{ width: `${Math.floor(progress)}%` }}
        />
      </div>
      <span className="text-sm font-semibold text-gray-600">
        {Math.floor(progress)}%
      </span>
    </div>
  );
}

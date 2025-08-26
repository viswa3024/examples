"use client";

import { useEffect, useRef, useState } from "react";

type Props = {
  children: React.ReactNode;
  className?: string;
  thumbColor?: string; // tailwind color (bg-gray-500 etc.)
  thumbWidth?: number; // px width
};

export default function CustomScrollbar({
  children,
  className = "",
  thumbColor = "bg-gray-500",
  thumbWidth = 2,
}: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const thumbRef = useRef<HTMLDivElement | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [startY, setStartY] = useState(0);
  const [startScroll, setStartScroll] = useState(0);

  // update thumb size & position
  const updateThumb = () => {
    const container = containerRef.current;
    const thumb = thumbRef.current;
    if (!container || !thumb) return;

    const containerHeight = container.clientHeight;
    const contentHeight = container.scrollHeight;
    const scrollTop = container.scrollTop;

    const thumbHeight = Math.max(
      (containerHeight * containerHeight) / contentHeight,
      20
    );
    const scrollRatio = scrollTop / (contentHeight - containerHeight);

    thumb.style.height = `${thumbHeight}px`;
    thumb.style.top = `${scrollRatio * (containerHeight - thumbHeight)}px`;
  };

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    updateThumb();
    container.addEventListener("scroll", updateThumb);
    window.addEventListener("resize", updateThumb);

    return () => {
      container.removeEventListener("scroll", updateThumb);
      window.removeEventListener("resize", updateThumb);
    };
  }, []);

  // handle dragging
  useEffect(() => {
    const container = containerRef.current;
    const thumb = thumbRef.current;
    if (!container || !thumb) return;

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const containerHeight = container.clientHeight;
      const contentHeight = container.scrollHeight;
      const thumbHeight = thumb.offsetHeight;
      const maxScroll = contentHeight - containerHeight;

      const delta = e.clientY - startY;
      const scrollDelta = (delta / (containerHeight - thumbHeight)) * maxScroll;
      container.scrollTop = startScroll + scrollDelta;
    };

    const onMouseUp = () => {
      setIsDragging(false);
      document.body.style.userSelect = "";
    };

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);

    return () => {
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
    };
  }, [isDragging, startY, startScroll]);

  return (
    <div className={`relative w-full h-full ${className}`}>
      {/* Scrollable container (native scrollbar hidden) */}
      <div
        ref={containerRef}
        className="
          w-full h-full overflow-auto pr-3 scroll-hide
          [scrollbar-width:none] [-ms-overflow-style:none]
        "
      >
        {children}
      </div>

      {/* Fake scrollbar */}
      <div
        className="absolute top-0 right-1 h-full bg-transparent"
        style={{ width: `${thumbWidth}px` }}
      >
        <div
          ref={thumbRef}
          className={`absolute top-0 w-full rounded cursor-pointer transition-colors duration-150 ${thumbColor}`}
          onMouseDown={(e) => {
            setIsDragging(true);
            setStartY(e.clientY);
            setStartScroll(containerRef.current?.scrollTop || 0);
            document.body.style.userSelect = "none";
          }}
        />
      </div>
    </div>
  );
}

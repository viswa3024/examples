'use client';

import { ChevronDown } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

type Option = {
  key: string;
  label: string;
};

type SelectProps = {
  label?: string;
  options: Option[];
  value: string;
  onChange: (key: string) => void;
  className?: string;
  isUseCreatePortal?: boolean; // toggle for portal
};

export default function CustomSelect({
  label,
  options,
  value,
  onChange,
  className = "",
  isUseCreatePortal = false,
}: SelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const dropdownRef = useRef<HTMLUListElement>(null);
  const [dropdownStyle, setDropdownStyle] = useState<React.CSSProperties>({});
  const rafRef = useRef<number | null>(null);
  const scrollParentsRef = useRef<(HTMLElement | Window)[]>([]);

  const selected = options.find((opt) => opt.key === value);

  // Close dropdown when clicking outside (accounts for portal dropdown too)
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Node;
      if (
        ref.current &&
        !ref.current.contains(target) &&
        (!dropdownRef.current || !dropdownRef.current.contains(target))
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Find scrollable ancestors to track overflow scroll
  const getScrollParents = (el: HTMLElement | null) => {
    const parents: (HTMLElement | Window)[] = [window];
    let parent = el?.parentElement || null;
    const regex = /(auto|scroll|overlay)/;
    while (parent) {
      const { overflow, overflowY, overflowX } = getComputedStyle(parent);
      if (regex.test(`${overflow}${overflowY}${overflowX}`)) parents.push(parent);
      parent = parent.parentElement;
    }
    return parents;
  };

  // Position updater (handles scroll/resize/zoom and flips if needed)
  const updateDropdownPosition = () => {
    if (!isUseCreatePortal || !isOpen || !ref.current) return;

    const rect = ref.current.getBoundingClientRect();
    const viewportH = window.innerHeight;
    const scrollY = window.scrollY;
    const scrollX = window.scrollX;

    // Measure dropdown height (fallback to max height if not rendered yet)
    const MAX_H = 240; // tailwind max-h-60 ~= 240px
    const measuredH = dropdownRef.current?.offsetHeight ?? MAX_H;

    // Prefer opening downward; flip up if not enough space below
    const spaceBelow = viewportH - rect.bottom;
    const spaceAbove = rect.top;
    let top: number;

    if (spaceBelow < Math.min(measuredH, MAX_H) && spaceAbove > spaceBelow) {
      // open upward
      top = rect.top + scrollY - Math.min(measuredH, MAX_H);
    } else {
      // open downward
      top = rect.bottom + scrollY;
    }

    const left = rect.left + scrollX;
    const width = rect.width;

    setDropdownStyle({
      position: 'fixed',
      top,
      left,
      width,
      zIndex: 50,
    });
  };

  const scheduleUpdate = () => {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    rafRef.current = requestAnimationFrame(updateDropdownPosition);
  };

  // Update position when opening and while open (scroll/resize/zoom/size changes)
  useEffect(() => {
    if (!isUseCreatePortal || !isOpen) return;

    // Initial position
    scheduleUpdate();

    // Track scroll on window + all scrollable ancestors
    const parents = getScrollParents(ref.current);
    scrollParentsRef.current = parents;

    parents.forEach((p) => (p as any).addEventListener('scroll', scheduleUpdate, { passive: true }));
    window.addEventListener('resize', scheduleUpdate);

    // Observe size changes of trigger and dropdown
    const ro = new ResizeObserver(scheduleUpdate);
    if (ref.current) ro.observe(ref.current);
    if (dropdownRef.current) ro.observe(dropdownRef.current);

    return () => {
      parents.forEach((p) => (p as any).removeEventListener('scroll', scheduleUpdate));
      window.removeEventListener('resize', scheduleUpdate);
      ro.disconnect();
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [isOpen, isUseCreatePortal, options.length]);

  // Recompute position if label/className changes layout subtly
  useEffect(() => {
    if (isUseCreatePortal && isOpen) scheduleUpdate();
  }, [label, className]);

  const dropdown = (
    <ul
      ref={dropdownRef}
      className="bg-white border border-gray-200 rounded shadow-md max-h-60 overflow-y-auto"
      style={isUseCreatePortal ? dropdownStyle : {}}
    >
      {options.map((option) => (
        <li
          key={option.key}
          onClick={() => {
            onChange(option.key);
            setIsOpen(false);
          }}
          className={`px-4 py-2 cursor-pointer hover:bg-blue-100 transition ${
            option.key === value ? 'bg-blue-50 font-semibold text-blue-600' : ''
          }`}
        >
          {option.label}
        </li>
      ))}
    </ul>
  );

  return (
    <div className={`relative w-full ${className}`} ref={ref}>
      {label && <label className="block text-gray-700 font-medium mb-1">{label}</label>}

      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className="w-full border border-gray-300 rounded px-3 py-2 text-left flex justify-between items-center bg-white shadow-sm"
      >
        <span className={selected ? "text-gray-800" : "text-gray-400"}>
          {selected?.label || 'Select...'}
        </span>
        <ChevronDown className="h-4 w-4 text-gray-500" />
      </button>

      {isOpen && (isUseCreatePortal ? createPortal(dropdown, document.body) : dropdown)}
    </div>
  );
}

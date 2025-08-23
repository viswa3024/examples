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
  isUseCreatePortal?: boolean; // 🔹 new param
};

export default function CustomSelect({
  label,
  options,
  value,
  onChange,
  className = "",
  isUseCreatePortal = false, // default false
}: SelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const [dropdownStyle, setDropdownStyle] = useState<React.CSSProperties>({});

  const selected = options.find((opt) => opt.key === value);

  // 🔹 Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // 🔹 Update dropdown position when opened (only for portal mode)
  useEffect(() => {
    if (isUseCreatePortal && isOpen && ref.current) {
      const rect = ref.current.getBoundingClientRect();
      setDropdownStyle({
        position: 'fixed',
        top: rect.bottom + window.scrollY,
        left: rect.left + window.scrollX,
        width: rect.width,
        zIndex: 50,
      });
    }
  }, [isOpen, isUseCreatePortal]);

  // 🔹 Dropdown content
  const dropdown = (
    <ul
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

      {isOpen &&
        (isUseCreatePortal ? createPortal(dropdown, document.body) : dropdown)}
    </div>
  );
}

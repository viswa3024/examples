import React, { useState } from 'react';

const YearSelect = ({ startYear, endYear, onYearChange }) => {
  const [selectedYear, setSelectedYear] = useState('');

  const generateYearOptions = () => {
    const options = [];
    for (let year = startYear; year <= endYear; year++) {
      options.push(<option key={year} value={year}>{year}</option>);
    }
    return options;
  };

  const handleChange = (e) => {
    const year = e.target.value;
    setSelectedYear(year);
    onYearChange(year);
  };

  return (
    <select value={selectedYear} onChange={handleChange}>
      <option value="">Select a year</option>
      {generateYearOptions()}
    </select>
  );
};

export default YearSelect;

// src/components/Calendar.js
import React, { useState } from 'react';
import moment from 'moment';
import './Calendar.css';

const Calendar = () => {
  const [selectedDateTime, setSelectedDateTime] = useState(moment().format('YYYY-MM-DDTHH:mm'));

  const handleDateTimeChange = (e) => {
    setSelectedDateTime(e.target.value);
  };

  const formattedDateTime = moment(selectedDateTime).format('MMMM Do, YYYY, h:mm A');

  return (
    <div className="calendar">
      <div className="datetime-picker">
        <label htmlFor="datetime">Select Date and Time: </label>
        <div className="input-with-icon">
          <input
            type="datetime-local"
            id="datetime"
            value={selectedDateTime}
            onChange={handleDateTimeChange}
          />
          <i className="fas fa-calendar-alt"></i>
        </div>
        <div className="formatted-datetime">
          Selected Date and Time: {formattedDateTime}
        </div>
      </div>
    </div>
  );
};

export default Calendar;

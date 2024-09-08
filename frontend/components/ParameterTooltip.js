import React, { useState } from 'react';

const ParameterTooltip = ({ explanation, example }) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div className="relative inline-block ml-2">
      <button
        type="button"
        className="text-gray-500 hover:text-gray-700"
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
        </svg>
      </button>
      {isVisible && (
        <div className="absolute z-10 w-64 px-4 py-2 text-sm text-gray-500 bg-white border border-gray-200 rounded-lg shadow-lg">
          <p className="mb-2">{explanation}</p>
          {example && (
            <p className="font-semibold">
              Example: <span className="font-normal">{example}</span>
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default ParameterTooltip;
// src/components/UploadForm.js
import React, { useState, useEffect } from 'react';

const UploadForm = ({ onFileUpload, resetTrigger }) => {
  const [realTimeFile, setRealTimeFile] = useState(null);
  const [historicalFile, setHistoricalFile] = useState(null);

  // Reset file states when resetTrigger changes
  useEffect(() => {
    setRealTimeFile(null);
    setHistoricalFile(null);
    // Clear the file input elements' values
    document.getElementById('real-time-upload').value = '';
    document.getElementById('historical-upload').value = '';
  }, [resetTrigger]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onFileUpload(realTimeFile, historicalFile);
  };

  return (
    <section className="upload-section">
      <form onSubmit={handleSubmit}>
        <div className="upload-group">
          <label htmlFor="real-time-upload" className="upload-label">RealTime Data:</label>
          <input
            type="file"
            id="real-time-upload"
            accept=".csv"
            onChange={(e) => setRealTimeFile(e.target.files[0])}
            className="upload-input"
          />
        </div>
        <div className="upload-group">
          <label htmlFor="historical-upload" className="upload-label">Historical Data:</label>
          <input
            type="file"
            id="historical-upload"
            accept=".csv"
            onChange={(e) => setHistoricalFile(e.target.files[0])}
            className="upload-input"
          />
        </div>
        <button type="submit" className="upload-button">Upload & Reconcile</button>
      </form>
    </section>
  );
};

export default UploadForm;
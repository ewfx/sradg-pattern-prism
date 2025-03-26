// src/App.js
import React, { useState } from 'react';
import Header from './components/Header';
import UploadForm from './components/UploadForm';
import ErrorMessage from './components/ErrorMessage';
import ResultsTable from './components/ResultsTable';
import Tabs from './components/Tabs';
import Spinner from './components/Spinner';
import './App.css';

const App = () => {
  const [ihubResults, setIhubResults] = useState([]);
  const [catalystResults, setCatalystResults] = useState([]);
  const [ihubError, setIhubError] = useState('');
  const [catalystError, setCatalystError] = useState('');
  const [activeTab, setActiveTab] = useState('IHub Reconciliation');
  const [loading, setLoading] = useState(false);

  const handleIhubFileUpload = async (realTimeFile, historicalFile) => {
    if (!realTimeFile || !realTimeFile.name.endsWith('.csv') || 
        !historicalFile || !historicalFile.name.endsWith('.csv')) {
      setIhubError('Please upload valid RealTime_Data.csv and Historical_Data.csv files.');
      setIhubResults([]);
      return;
    }

    setLoading(true);
    setIhubError('');
    setIhubResults([]);

    const formData = new FormData();
    formData.append('realTimeData', realTimeFile);
    formData.append('historicalData', historicalFile);

    try {
      const response = await fetch('http://localhost:5000/reconcile', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setIhubResults(data);
        setIhubError('');
      } else {
        throw new Error(data.error || 'Failed to process CSVs');
      }
    } catch (err) {
      setIhubError(err.message);
      setIhubResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCatalystFileUpload = async (realTimeFile, historicalFile) => {
    if (!realTimeFile || !realTimeFile.name.endsWith('.csv') || 
        !historicalFile || !historicalFile.name.endsWith('.csv')) {
      setCatalystError('Please upload valid RealTime_Catalyst.csv and Historical_Catalyst.csv files.');
      setCatalystResults([]);
      return;
    }

    setLoading(true);
    setCatalystError('');
    setCatalystResults([]);

    const formData = new FormData();
    formData.append('realTimeData', realTimeFile);
    formData.append('historicalData', historicalFile);

    try {
      const response = await fetch('http://localhost:5000/reconcile-catalyst', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setCatalystResults(data);
        setCatalystError('');
      } else {
        throw new Error(data.error || 'Failed to process CSVs');
      }
    } catch (err) {
      setCatalystError(err.message);
      setCatalystResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Header />
      {loading && <Spinner />}
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab}>
        {/* IHub Reconciliation Tab */}
        <div>
          <UploadForm onFileUpload={handleIhubFileUpload} resetTrigger={activeTab} />
          <ErrorMessage message={ihubError} />
          <ResultsTable results={ihubResults} />
        </div>
        {/* Catalyst Reconciliation Tab */}
        <div>
          <UploadForm onFileUpload={handleCatalystFileUpload} resetTrigger={activeTab} />
          <ErrorMessage message={catalystError} />
          <ResultsTable results={catalystResults} />
        </div>
      </Tabs>
    </div>
  );
};

export default App;
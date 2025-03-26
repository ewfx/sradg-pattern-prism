// src/components/ResultsTable.js
import React from 'react';
import IHubResultsTable from './IHubResultsTable';
import CatalystResultsTable from './CatalystResultsTable';

const ResultsTable = ({ results }) => {
  if (results.length === 0) return null;

  const isCatalyst = results[0].hasOwnProperty('Price Catalyst');

  return isCatalyst ? (
    <CatalystResultsTable results={results} />
  ) : (
    <IHubResultsTable results={results} />
  );
};

export default ResultsTable;
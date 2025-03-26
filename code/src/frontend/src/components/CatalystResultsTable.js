// src/components/CatalystResultsTable.js
import React from 'react';
import TableWrapper from './TableWrapper';
import TableHeader from './TableHeader';
import TableRow from './TableRow';

const CatalystResultsTable = ({ results }) => {
  const columns = [
    { key: 'Recon Date', label: 'Recon Date' },
    { key: 'Trade ID', label: 'Trade ID' },
    { key: 'Inventory Code', label: 'Inventory Code' },
    { key: 'CUSIP', label: 'CUSIP' },
    { key: 'Trade Date', label: 'Trade Date' },
    { key: 'Settlement Date', label: 'Settlement Date' },
    { key: 'Buy or Sell', label: 'Buy or Sell' },
    { key: 'Price Catalyst', label: 'Price Catalyst' },
    { key: 'Price Impact', label: 'Price Impact' },
    { key: 'Quantity Catalyst', label: 'Quantity Catalyst' },
    { key: 'Quantity Impact', label: 'Quantity Impact' },
    { key: 'Price Difference', label: 'Price Difference' },
    { key: 'Quantity Difference', label: 'Quantity Difference' },
    { key: 'Match Status', label: 'Match Status' },
    { key: 'Price Anomaly', label: 'Price Anomaly', transform: (val) => (val ? 'Yes' : 'No') },
    { key: 'Quantity Anomaly', label: 'Anomaly', transform: (val) => (val ? 'Yes' : 'No') },
    { key: 'comment', label: 'comment' },
  ];

  // Highlight rows where either Price Anomaly or Quantity Anomaly is true
  const highlightCondition = (row) => row['Price Anomaly'] || row['Quantity Anomaly'];

  return (
    <TableWrapper>
      <TableHeader columns={columns.map(col => col.label)} />
      <tbody>
        {results.map((result, index) => (
          <TableRow
            key={index}
            row={{
              ...result,
              'Price Anomaly': result['Price Anomaly'] ? 'Yes' : 'No', // Transform boolean to string
              'Quantity Anomaly': result['Quantity Anomaly'] ? 'Yes' : 'No', // Transform boolean to string
            }}
            columns={columns}
            highlightCondition={highlightCondition}
          />
        ))}
      </tbody>
    </TableWrapper>
  );
};

export default CatalystResultsTable;
// src/components/IHubResultsTable.js
import React from 'react';
import TableWrapper from './TableWrapper';
import TableHeader from './TableHeader';
import TableRow from './TableRow';

const IHubResultsTable = ({ results }) => {
  const columns = [
    { key: 'As of Date', label: 'As of Date' },
    { key: 'Company', label: 'Company' },
    { key: 'Account', label: 'Account' },
    { key: 'GL Balance', label: 'GL Balance' },
    { key: 'IHub Balance', label: 'IHub Balance' },
    { key: 'Match Status', label: 'Match Status' },
    { key: 'Balance Difference', label: 'Balance Difference' },
    { key: 'Anomaly', label: 'Anomaly', transform: (val) => (val ? 'Yes' : 'No') },
    { key: 'Comments', label: 'Comments' },
  ];

  const highlightCondition = (row) => row.Anomaly;

  return (
    <TableWrapper>
      <TableHeader columns={columns.map(col => col.label)} />
      <tbody>
        {results.map((result, index) => (
          <TableRow
            key={index}
            row={{
              ...result,
              Anomaly: result.Anomaly ? 'Yes' : 'No', // Transform boolean to string
            }}
            columns={columns}
            highlightCondition={highlightCondition}
          />
        ))}
      </tbody>
    </TableWrapper>
  );
};

export default IHubResultsTable;
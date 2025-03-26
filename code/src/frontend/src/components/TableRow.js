// src/components/TableRow.js
import React from 'react';

const TableRow = ({ row, columns, highlightCondition }) => (
  <tr className={highlightCondition(row) ? 'anomaly-row' : ''}>
    {columns.map((col, index) => {
      const value = row[col.key];
      const className = col.key === 'Match Status' 
        ? (value === 'Match' ? 'match-status' : 'break-status') 
        : '';
      return <td key={index} className={className}>{value}</td>;
    })}
  </tr>
);

export default TableRow;
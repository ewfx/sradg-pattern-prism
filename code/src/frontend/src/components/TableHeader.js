// src/components/TableHeader.js
import React from 'react';

const TableHeader = ({ columns }) => (
  <thead>
    <tr>
      {columns.map((col, index) => (
        <th key={index}>{col}</th>
      ))}
    </tr>
  </thead>
);

export default TableHeader;
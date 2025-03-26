// src/components/TableWrapper.js
import React from 'react';

const TableWrapper = ({ children }) => (
  <section className="results-section">
    <div className="table-wrapper">
      <table className="results-table">{children}</table>
    </div>
  </section>
);

export default TableWrapper;
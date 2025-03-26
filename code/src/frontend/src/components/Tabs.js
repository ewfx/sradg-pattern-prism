import React from 'react';

const Tabs = ({ activeTab, setActiveTab, children }) => {
  const tabs = ['IHub Reconciliation', 'Catalyst Reconciliation'];

  return (
    <div className="tabs-container">
      <div className="tabs-header">
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`tab-button ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="tabs-content">
        {children[activeTab === 'IHub Reconciliation' ? 0 : 1]}
      </div>
    </div>
  );
};

export default Tabs;
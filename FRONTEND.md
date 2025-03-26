# Frontend Documentation

This document outlines the frontend structure and components of the reconciliation application built with React. The frontend interacts with a Flask backend to upload CSV files and display reconciliation results.

src/
components/
TableWrapper.js       # Reusable table wrapper with styling
TableHeader.js        # Generic table header component
TableRow.js           # Generic table row component
IHubResultsTable.js   # IHub-specific table display
CatalystResultsTable.js # Catalyst-specific table display with anomaly columns
ResultsTable.js       # Main component to route results to IHub or Catalyst tables
Header.js             # Application header
UploadForm.js         # File upload form with reset on tab switch
ErrorMessage.js       # Error display component
Tabs.js               # Tab navigation component
Spinner.js            # Loading spinner
App.js                 # Main application component
App.css                # Styles for the application


## Components

### `App.js`
- **Purpose:** Main entry point, manages state, and orchestrates tab switching and file uploads.
- **State:**
  - `ihubResults`, `catalystResults`: Store reconciliation results.
  - `ihubError`, `catalystError`: Store error messages.
  - `activeTab`: Tracks the current tab ("IHub Reconciliation" or "Catalyst Reconciliation").
  - `loading`: Indicates processing status.
- **Functions:**
  - `handleIhubFileUpload`: Sends IHub CSV files to `/reconcile` endpoint.
  - `handleCatalystFileUpload`: Sends Catalyst CSV files to `/reconcile-catalyst` endpoint.
- **Features:** Clears file inputs on tab switch via `resetTrigger` prop.

### `UploadForm.js`
- **Purpose:** Handles CSV file uploads for both tabs.
- **Props:**
  - `onFileUpload`: Callback to process uploaded files.
  - `resetTrigger`: Resets file inputs when tab changes (uses `activeTab`).
- **State:** `realTimeFile`, `historicalFile` for selected files.
- **Features:** Resets inputs using `useEffect` when `resetTrigger` changes.

### `ResultsTable.js`
- **Purpose:** Routes results to either `IHubResultsTable` or `CatalystResultsTable` based on data type.
- **Logic:** Checks if results contain "Price Catalyst" to determine Catalyst data.

### `IHubResultsTable.js`
- **Purpose:** Displays IHub reconciliation results.
- **Columns:** As of Date, Company, Account, GL Balance, IHub Balance, Match Status, Balance Difference, Anomaly, Comments.
- **Features:** Highlights rows with `Anomaly: true`.

### `CatalystResultsTable.js`
- **Purpose:** Displays Catalyst reconciliation results with anomaly details.
- **Columns:** Recon Date, Trade ID, Inventory Code, CUSIP, Trade Date, Settlement Date, Buy or Sell, Price Catalyst, Price Impact, Quantity Catalyst, Quantity Impact, Price Difference, Quantity Difference, Match Status, Price Anomaly, Quantity Anomaly, comment.
- **Features:** Highlights rows where `Price Anomaly` or `Quantity Anomaly` is `true`, transforms booleans to "Yes"/"No".

### `TableWrapper.js`, `TableHeader.js`, `TableRow.js`
- **Purpose:** Reusable components for table structure.
- **TableWrapper:** Applies common styling.
- **TableHeader:** Renders column headers.
- **TableRow:** Renders row data with conditional styling (e.g., `anomaly-row`, `match-status`).

### `Header.js`, `ErrorMessage.js`, `Tabs.js`, `Spinner.js`
- **Header:** Static app title.
- **ErrorMessage:** Displays error messages.
- **Tabs:** Manages tab navigation.
- **Spinner:** Shows loading animation during processing.

## Styles (`App.css`)
- **Classes:**
  - `results-section`, `table-wrapper`, `results-table`: Table styling.
  - `anomaly-row`: Highlights anomalous rows.
  - `match-status`, `break-status`: Styles for Match/Break status.

## Usage
1. **Run the Frontend:**
   - `npm install` to install dependencies (React, etc.).
   - `npm start` to launch at `http://localhost:3000`.
2. **Interact:**
   - Switch between "IHub Reconciliation" and "Catalyst Reconciliation" tabs.
   - Upload `RealTime_Data.csv` and `Historical_Data.csv` for IHub.
   - Upload `RealTime_Catalyst.csv` and `Historical_Catalyst.csv` for Catalyst.
   - View results and anomalies in the respective tables.

## Notes
- File inputs reset on tab switch to prevent reuse of previous files.
- Anomalies in Catalyst tab are highlighted and logged in Jira (backend-handled).

## Directory Structure
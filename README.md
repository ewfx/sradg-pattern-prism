# IHub_Reconciliation

# Reconciliation Application

This is a full-stack application for reconciling financial data from CSV files, detecting anomalies, and integrating with Jira for anomaly reporting. It consists of a React frontend and a Flask backend.

## Overview
- **Frontend:** A React-based UI for uploading CSV files and displaying reconciliation results in tabular format.
- **Backend:** A Flask API that processes CSV uploads, performs reconciliation, detects anomalies, and creates Jira issues for anomalies in the Catalyst Reconciliation tab.

## Prerequisites
- **Frontend:** Node.js (v16+), npm
- **Backend:** Python 3.8+, pip
- **Jira:** A Jira instance with API token for anomaly reporting (optional for IHub functionality).

## Installation
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd reconciliation-app
   
Frontend Setup:
Navigate to the frontend directory (or src if flat structure).
Install dependencies: npm install
Start the app: npm start
Backend Setup:
Navigate to the reconciliation_app directory.
Install dependencies: pip install Flask pandas transformers torch numpy requests
Update config.py with Jira credentials.
Start the server: python app.py
Usage
Run the Application:
Backend: http://localhost:5000
Frontend: http://localhost:3000
Upload Files:
IHub Reconciliation: Upload RealTime_Data.csv and Historical_Data.csv.
Catalyst Reconciliation: Upload RealTime_Catalyst.csv and Historical_Catalyst.csv.
View Results:
Results and anomalies are displayed in the respective tabs.
Anomalies in Catalyst tab trigger Jira issues (if configured).
Documentation
Frontend Documentation: Details the React components, structure, and usage.
Backend Documentation: Describes the Flask API, file structure, anomaly detection, and Jira integration.
Features
File Upload: Supports CSV uploads with tab-specific validation.
Reconciliation: Compares real-time and historical data for IHub and Catalyst.
Anomaly Detection: Flags outliers based on historical trends.
Jira Integration: Creates issues for Catalyst anomalies with detailed descriptions.

# END
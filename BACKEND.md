# Backend Documentation

This document describes the backend structure of the reconciliation application built with Flask. It processes CSV uploads, performs reconciliation, detects anomalies, and integrates with Jira for anomaly reporting.

reconciliation_app/
app.py             # Main Flask app and endpoints
config.py          # Configuration (e.g., Jira settings)
utils.py           # Utility functions (status, anomaly detection)
comments.py        # Comment generation logic
reconciliation.py  # Reconciliation logic for IHub and Catalyst
jira.py            # Jira integration for anomaly reporting
app.log            # Log file (generated during runtime)


## Files

### `app.py`
- **Purpose:** Main Flask application with endpoints `/reconcile` and `/reconcile-catalyst`.
- **Endpoints:**
  - `/reconcile`: Processes IHub CSV files.
  - `/reconcile-catalyst`: Processes Catalyst CSV files, detects anomalies, and creates Jira issues.
- **Dependencies:** `Flask`, `pandas`, `reconciliation` module.
- **Features:** CORS support, logging, error handling.

### `config.py`
- **Purpose:** Stores configuration variables.
- **Variables:**
  - `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`: Jira credentials and settings.
- **Usage:** Replace placeholders with your Jira details.

### `utils.py`
- **Purpose:** Utility functions for status and anomaly detection.
- **Functions:**
  - `determine_match_status_ihub(gl_balance, ihub_balance)`: Returns "Match" or "Break" for IHub.
  - `determine_match_status_catalyst(price_diff, quantity_diff)`: Returns "Match" or "Break" for Catalyst.
  - `detect_anomaly(historical_diffs, current_diff, identifier, idx, threshold, z_threshold)`: Detects anomalies using z-score (default 2) and threshold (default 1000, adjusted for Catalyst).

### `comments.py`
- **Purpose:** Generates comments for reconciliation results using DistilBERT sentiment analysis.
- **Functions:**
  - `generate_comment(diff_type, diff_value, is_anomaly, historical_diffs)`: For IHub results.
  - `generate_catalyst_comment(price_diff, quantity_diff, price_anomaly, quantity_anomaly, historical_price_diffs, historical_quantity_diffs)`: For Catalyst results with anomaly details.
- **Dependency:** `transformers` (DistilBERT).

### `reconciliation.py`
- **Purpose:** Core reconciliation logic for IHub and Catalyst.
- **Functions:**
  - `reconcile_ihub_data(real_time_df, historical_df)`: Reconciles IHub data, detects balance anomalies.
  - `reconcile_catalyst_data(real_time_df, historical_df)`: Reconciles Catalyst data, detects price/quantity anomalies, and triggers Jira issues for anomalies.
- **Dependencies:** `pandas`, `utils`, `comments`, `jira`.

### `jira.py`
- **Purpose:** Creates Jira issues for Catalyst anomalies.
- **Function:**
  - `create_jira_issue(trade_id, price_diff, quantity_diff, price_anomaly, quantity_anomaly, comment)`: Posts to Jira REST API.
- **Dependencies:** `requests`, `config`.

## Usage
1. **Install Dependencies:**
   - `pip install Flask pandas transformers torch numpy requests`
2. **Configure:**
   - Update `config.py` with Jira credentials.
3. **Run the Backend:**
   - From `reconciliation_app/`, run `python app.py`.
   - Runs on `http://localhost:5000`.
4. **Test Endpoints:**
   - `/reconcile`: Upload `RealTime_Data.csv` and `Historical_Data.csv`.
   - `/reconcile-catalyst`: Upload `RealTime_Catalyst.csv` and `Historical_Catalyst.csv`.

## Anomaly Detection
- **IHub:** Detects anomalies in `Balance Difference` (threshold=1000, z_threshold=2).
- **Catalyst:**
  - Detects anomalies in `Price Difference` (threshold=10) and `Quantity Difference` (threshold=50).
  - Creates Jira issues for rows where `Price Anomaly` or `Quantity Anomaly` is `true`.
  - Jira issue includes Trade ID, differences, anomaly status, and comment.

## Logging
- **File:** `app.log`
- **Level:** DEBUG
- **Details:** Logs file processing, anomaly detection (z-scores), sentiment analysis, and Jira interactions.

## Notes
- Ensure Jira credentials are valid to avoid integration errors.
- Adjust anomaly thresholds in `detect_anomaly` calls for stricter/looser detection.
- Backend expects CSV files with specific columns; errors are returned if columns are missing.

## Directory Structure
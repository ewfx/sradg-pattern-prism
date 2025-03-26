import pandas as pd
import datetime
import logging
from utils import determine_match_status_ihub, determine_match_status_catalyst, detect_anomaly
from comments import generate_comment, generate_catalyst_comment
from jira import create_jira_issue, create_jira_issue_ihub

logger = logging.getLogger(__name__)

# IHub Reconciliation logic
def reconcile_ihub_data(real_time_df, historical_df):
    required_cols = ['As of Date', 'Company', 'Account', 'AU', 'Currency', 'Secondary Account', 'GL Balance', 'IHub Balance']
    logger.debug(f"IHub Real-time columns: {list(real_time_df.columns)}")
    logger.debug(f"IHub Historical columns: {list(historical_df.columns)}")
    if not all(col in real_time_df.columns for col in required_cols) or \
       not all(col in historical_df.columns for col in required_cols):
        missing_real_time = [col for col in required_cols if col not in real_time_df.columns]
        missing_historical = [col for col in required_cols if col not in historical_df.columns]
        logger.error(f"Missing columns - Real-time: {missing_real_time}, Historical: {missing_historical}")
        return None, {'error': f'Missing required columns in one or both files - Real-time: {missing_real_time}, Historical: {missing_historical}'}

    historical_trends = {}
    for key, group in historical_df.groupby(['Account', 'AU', 'Currency', 'Secondary Account']):
        diffs = (group['GL Balance'] - group['IHub Balance']).tolist()
        historical_trends[tuple(str(k) for k in key)] = diffs
        logger.debug(f"Historical trends for {key}: {diffs}")

    results = []
    for idx, row in real_time_df.iterrows():
        gl_balance = float(row['GL Balance'])
        ihub_balance = float(row['IHub Balance'])
        balance_diff = gl_balance - ihub_balance
        match_status = determine_match_status_ihub(gl_balance, ihub_balance)
        
        key = (str(row['Account']), str(row['AU']), str(row['Currency']), str(row['Secondary Account']))
        historical_diffs = historical_trends.get(key, [])
        is_anomaly = detect_anomaly(historical_diffs, balance_diff, row['Account'], idx)
        comment = generate_comment("Balance", balance_diff, is_anomaly, historical_diffs)

       # Create Jira issue if anomaly is detected
        if is_anomaly:
            jira_issue_key = create_jira_issue_ihub(row['Account'], balance_diff, is_anomaly, comment)
            if jira_issue_key:
                comment += f" (Jira Issue: {jira_issue_key})"

        as_of_date = row['As of Date']
        if isinstance(as_of_date, (pd.Timestamp, datetime.date)):
            as_of_date = as_of_date.strftime("%Y-%m-%d")
        else:
            as_of_date = str(as_of_date)

        result = {
            'As of Date': as_of_date,
            'Company': str(row['Company']),
            'Account': str(row['Account']),
            'AU': str(row['AU']),
            'Currency': str(row['Currency']),
            'Secondary Account': str(row['Secondary Account']),
            'GL Balance': float(gl_balance),
            'IHub Balance': float(ihub_balance),
            'Balance Difference': float(balance_diff),
            'Match Status': match_status,
            'Anomaly': bool(is_anomaly),
            'Comments': comment
        }
        results.append(result)
        logger.debug(f"Processed row {idx}: Account={row['Account']}, Diff={balance_diff}, Anomaly={is_anomaly}")

    return results, None

# Catalyst Reconciliation logic with anomaly detection and Jira integration
def reconcile_catalyst_data(real_time_df, historical_df):
    required_cols = ['Recon Date', 'Trade ID', 'Inventory Code', 'CUSIP', 'Trade Date', 'Settlement Date', 
                     'Buy or Sell', 'Price Catalyst', 'Price Impact', 'Quantity Catalyst', 'Quantity Impact']
    logger.debug(f"Catalyst Real-time columns: {list(real_time_df.columns)}")
    logger.debug(f"Catalyst Historical columns: {list(historical_df.columns)}")
    if not all(col in real_time_df.columns for col in required_cols) or \
       not all(col in historical_df.columns for col in required_cols):
        missing_real_time = [col for col in required_cols if col not in real_time_df.columns]
        missing_historical = [col for col in required_cols if col not in historical_df.columns]
        logger.error(f"Missing columns - Real-time: {missing_real_time}, Historical: {missing_historical}")
        return None, {'error': f'Missing required columns in one or both files - Real-time: {missing_real_time}, Historical: {missing_historical}'}

    # Historical trends from Historical_Catalyst.csv
    historical_price_trends = {}
    historical_quantity_trends = {}
    for key, group in historical_df.groupby(['Trade ID', 'Inventory Code', 'CUSIP']):
        price_diffs = (group['Price Catalyst'] - group['Price Impact']).tolist()
        quantity_diffs = (group['Quantity Catalyst'] - group['Quantity Impact']).tolist()
        historical_price_trends[tuple(str(k) for k in key)] = price_diffs
        historical_quantity_trends[tuple(str(k) for k in key)] = quantity_diffs
        logger.debug(f"Historical price trends for {key}: {price_diffs}")
        logger.debug(f"Historical quantity trends for {key}: {quantity_diffs}")

    results = []
    for idx, row in real_time_df.iterrows():
        price_catalyst = float(row['Price Catalyst'])
        price_impact = float(row['Price Impact'])
        quantity_catalyst = float(row['Quantity Catalyst'])
        quantity_impact = float(row['Quantity Impact'])
        price_diff = price_catalyst - price_impact
        quantity_diff = quantity_catalyst - quantity_impact
        match_status = determine_match_status_catalyst(price_diff, quantity_diff)
        
        key = (str(row['Trade ID']), str(row['Inventory Code']), str(row['CUSIP']))
        historical_price_diffs = historical_price_trends.get(key, [])
        historical_quantity_diffs = historical_quantity_trends.get(key, [])
        
        # Detect anomalies based on historical data
        price_anomaly = detect_anomaly(historical_price_diffs, price_diff, row['Trade ID'], idx, threshold=10, z_threshold=2)
        quantity_anomaly = detect_anomaly(historical_quantity_diffs, quantity_diff, row['Trade ID'], idx, threshold=50, z_threshold=2)
        
        # Generate comment based on anomalies
        comment = generate_catalyst_comment(price_diff, quantity_diff, price_anomaly, quantity_anomaly, 
                                           historical_price_diffs, historical_quantity_diffs)
        logger.info(f"*********About to check Anomaly")
        # Create Jira issue if anomaly detected
        if price_anomaly or quantity_anomaly:
            logger.info(f"*********Create Jira Request for Trade Id:{row['Trade ID']}")
            jira_issue_key = create_jira_issue(row['Trade ID'], price_diff, quantity_diff, price_anomaly, quantity_anomaly, comment)
            if jira_issue_key:
                comment += f" (Jira Issue: {jira_issue_key})"

        recon_date = row['Recon Date']
        if isinstance(recon_date, (pd.Timestamp, datetime.date)):
            recon_date = recon_date.strftime("%Y-%m-%d")
        else:
            recon_date = str(recon_date)

        result = {
            'Recon Date': recon_date,
            'Trade ID': str(row['Trade ID']),
            'Inventory Code': str(row['Inventory Code']),
            'CUSIP': str(row['CUSIP']),
            'Trade Date': str(row['Trade Date']),
            'Settlement Date': str(row['Settlement Date']),
            'Buy or Sell': str(row['Buy or Sell']),
            'Price Catalyst': float(price_catalyst),
            'Price Impact': float(price_impact),
            'Quantity Catalyst': float(quantity_catalyst),
            'Quantity Impact': float(quantity_impact),
            'Price Difference': float(price_diff),
            'Quantity Difference': float(quantity_diff),
            'Match Status': match_status,
            'Price Anomaly': bool(price_anomaly),
            'Quantity Anomaly': bool(quantity_anomaly),
            'comment': comment
        }
        results.append(result)
        logger.debug(f"Processed row {idx}: Trade ID={row['Trade ID']}, Price Diff={price_diff}, Quantity Diff={quantity_diff}, Price Anomaly={price_anomaly}, Quantity Anomaly={quantity_anomaly}, Comment={comment}")

    return results, None
import logging
import numpy as np

logger = logging.getLogger(__name__)

# Match status function for IHub (balance-based)
def determine_match_status_ihub(gl_balance, ihub_balance):
    diff = gl_balance - ihub_balance
    return 'Match' if abs(diff) < 1 else 'Break'

# Match status function for Catalyst (price and quantity-based)
def determine_match_status_catalyst(price_diff, quantity_diff):
    return 'Match' if abs(price_diff) < 1 and quantity_diff == 0 else 'Break'

# Dynamic anomaly detection
def detect_anomaly(historical_diffs, current_diff, identifier, idx, threshold=1000, z_threshold=2):
    if len(historical_diffs) < 2:
        logger.debug(f"Insufficient historical data for {identifier} at index {idx}: {len(historical_diffs)} points")
        return abs(current_diff) > threshold
    
    historical_diffs_py = [float(d) for d in historical_diffs]
    mean_historical = sum(historical_diffs_py) / len(historical_diffs_py)
    std_dev_historical = float(np.std(historical_diffs_py)) if len(historical_diffs_py) > 1 else 0
    
    if std_dev_historical == 0:
        anomaly = abs(current_diff - mean_historical) > threshold
        logger.debug(f"Zero std dev for {identifier} at {idx}: diff={current_diff}, mean={mean_historical}, anomaly={anomaly}")
        return anomaly
    
    z_score = (current_diff - mean_historical) / std_dev_historical
    anomaly = abs(z_score) > z_threshold
    logger.debug(f"Z-score for {identifier} at {idx}: diff={current_diff}, mean={mean_historical}, std={std_dev_historical}, z_score={z_score}, anomaly={anomaly}")
    
    max_historical = max(historical_diffs_py)
    min_historical = min(historical_diffs_py)
    if current_diff > max_historical + threshold or current_diff < min_historical - threshold:
        logger.debug(f"Extreme deviation for {identifier} at {idx}: diff={current_diff}, max={max_historical}, min={min_historical}")
        anomaly = True
    
    return anomaly
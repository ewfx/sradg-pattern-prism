from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

# Load DistilBERT
try:
    nlp = pipeline("sentiment-analysis", model="distilbert-base-uncased", truncation=True)
    logger.info("DistilBERT model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load DistilBERT: {str(e)}")
    raise

# Generic comment generation for IHub
def generate_comment(diff_type, diff_value, is_anomaly, historical_diffs):
    mean_historical = sum(historical_diffs) / len(historical_diffs) if historical_diffs else 0
    diff_str = f"{diff_type} difference: {diff_value}, historical mean: {mean_historical}"
    sentiment = nlp(diff_str)[0]
    sentiment_label = sentiment['label']
    sentiment_score = sentiment['score']
    logger.debug(f"Sentiment for {diff_type} {diff_value}: label={sentiment_label}, score={sentiment_score}")

    if is_anomaly:
        if diff_value > 0:
            prefix = "Significant spike" if sentiment_label == 'POSITIVE' and sentiment_score > 0.7 else "Unexpected increase"
            return f"{prefix} in {diff_type.lower()} detected as anomaly from historical trends"
        elif diff_value < 0:
            prefix = "Significant drop" if sentiment_label == 'NEGATIVE' and sentiment_score > 0.7 else "Unexpected decrease"
            return f"{prefix} in {diff_type.lower()} detected as anomaly from historical trends"
        else:
            return f"Unusual variation in {diff_type.lower()} detected as anomaly from historical trends"
    elif abs(diff_value) < 1 and diff_value != 0:
        return f"Minor difference in {diff_type.lower()} within tolerance, consistent with historical patterns"
    elif diff_value == 0:
        return f"{diff_type} perfectly aligned with historical trends"
    else:
        if diff_value > mean_historical:
            prefix = "Gradual increase" if sentiment_label == 'POSITIVE' else "Slight rise"
            return f"{prefix} in {diff_type.lower()} within historical norms"
        elif diff_value < mean_historical:
            prefix = "Gradual decrease" if sentiment_label == 'NEGATIVE' else "Slight drop"
            return f"{prefix} in {diff_type.lower()} within historical norms"
        else:
            return f"{diff_type} consistent with historical trends"

# Generate comments for Catalyst
def generate_catalyst_comment(price_diff, quantity_diff, price_anomaly, quantity_anomaly, historical_price_diffs, historical_quantity_diffs):
    price_mean = sum(historical_price_diffs) / len(historical_price_diffs) if historical_price_diffs else 0
    quantity_mean = sum(historical_quantity_diffs) / len(historical_quantity_diffs) if historical_quantity_diffs else 0
    diff_str = f"Price diff: {price_diff}, historical price mean: {price_mean}; Quantity diff: {quantity_diff}, historical quantity mean: {quantity_mean}"
    sentiment = nlp(diff_str)[0]
    sentiment_label = sentiment['label']
    sentiment_score = sentiment['score']
    logger.debug(f"Sentiment for diff: {diff_str}, label={sentiment_label}, score={sentiment_score}")

    if price_anomaly and quantity_anomaly:
        return "Significant anomalies detected in both price and quantity based on historical trends"
    elif price_anomaly:
        if price_diff > price_mean:
            prefix = "Significant spike" if sentiment_label == 'POSITIVE' and sentiment_score > 0.7 else "Unexpected increase"
            return f"{prefix} in price difference detected as anomaly from historical trends"
        elif price_diff < price_mean:
            prefix = "Significant drop" if sentiment_label == 'NEGATIVE' and sentiment_score > 0.7 else "Unexpected decrease"
            return f"{prefix} in price difference detected as anomaly from historical trends"
        else:
            return "Unusual variation in price difference detected as anomaly from historical trends"
    elif quantity_anomaly:
        if quantity_diff > quantity_mean:
            prefix = "Significant spike" if sentiment_label == 'POSITIVE' and sentiment_score > 0.7 else "Unexpected increase"
            return f"{prefix} in quantity difference detected as anomaly from historical trends"
        elif quantity_diff < quantity_mean:
            prefix = "Significant drop" if sentiment_label == 'NEGATIVE' and sentiment_score > 0.7 else "Unexpected decrease"
            return f"{prefix} in quantity difference detected as anomaly from historical trends"
        else:
            return "Unusual variation in quantity difference detected as anomaly from historical trends"
    elif abs(price_diff) > abs(quantity_diff):
        if abs(price_diff) < 1:
            return "Minor price difference within tolerance, consistent with historical trends"
        elif price_diff == 0 and quantity_diff == 0:
            return "Price and quantity perfectly aligned with historical trends"
        elif price_diff > price_mean:
            return "Slight rise in price difference within historical norms"
        elif price_diff < price_mean:
            return "Slight drop in price difference within historical norms"
        else:
            return "Price difference consistent with historical trends"
    else:
        if abs(quantity_diff) < 1:
            return "Minor quantity difference within tolerance, consistent with historical trends"
        elif quantity_diff == 0 and price_diff == 0:
            return "Price and quantity perfectly aligned with historical trends"
        elif quantity_diff > quantity_mean:
            return "Slight rise in quantity difference within historical norms"
        elif quantity_diff < quantity_mean:
            return "Slight drop in quantity difference within historical norms"
        else:
            return "Quantity difference consistent with historical trends"
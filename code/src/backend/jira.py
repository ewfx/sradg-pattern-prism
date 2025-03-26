import requests
from requests.auth import HTTPBasicAuth
from config import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY
import logging

logger = logging.getLogger(__name__)


def create_jira_issue_ihub(account, balance_diff, is_anomaly, comment):
    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    description = (
        f"Anomaly detected for Account: {account}\n"
        f"Balance Difference: {balance_diff}\n"
        f"Anomaly: {'Yes' if is_anomaly else 'No'}\n"
        f"Comment: {comment}"
    )

    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": f"IHub Anomaly Detected for Account: {account}",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": 'Task'
            }
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        issue_key = response.json().get('key')
        logger.info(f"Jira issue created successfully for IHub: {issue_key}")
        return issue_key
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create Jira issue for IHub Account {account}: {str(e)}")
        return None

# Function to create a Jira issue
def create_jira_issue(trade_id, price_diff, quantity_diff, price_anomaly, quantity_anomaly, comment):
    
    JIRA_URL = 'https://newzalem.atlassian.net'
    JIRA_USERNAME = 'email here'
    JIRA_API_TOKEN = 'token here'
    JIRA_PROJECT_KEY = 'KAN'
    JIRA_ISSUE_TYPE = 'Task'

    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    description = (
        f"Anomaly detected for Trade ID: {trade_id}\n"
        f"Price Difference: {price_diff}\n"
        f"Quantity Difference: {quantity_diff}\n"
        f"Price Anomaly: {'Yes' if price_anomaly else 'No'}\n"
        f"Quantity Anomaly: {'Yes' if quantity_anomaly else 'No'}\n"
        f"Comment: {comment}"
    )

    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": f"Anomaly Detected for Trade ID: {trade_id}",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"  # Adjust issue type as needed (e.g., "Task", "Story")
            }
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        issue_key = response.json().get('key')
        logger.info(f"Jira issue created successfully: {issue_key}")
        return issue_key
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create Jira issue for Trade ID {trade_id}: {str(e)}")
        return None
from flask import Flask, request, jsonify
from reconciliation import reconcile_ihub_data, reconcile_catalyst_data
import logging
from io import StringIO
import pandas as pd

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

# IHub Reconciliation endpoint
@app.route('/reconcile', methods=['POST'])
def reconcile_ihub():
    logger.info("Received request to /reconcile")
    try:
        if 'realTimeData' not in request.files or 'historicalData' not in request.files:
            logger.error("Missing required files in request")
            return jsonify({'error': 'Both RealTime_Data.csv and Historical_Data.csv are required'}), 400

        real_time_file = request.files['realTimeData']
        historical_file = request.files['historicalData']
        logger.info(f"Files received: {real_time_file.filename}, {historical_file.filename}")

        if not real_time_file.filename.endswith('.csv') or not historical_file.filename.endswith('.csv'):
            logger.error("Invalid file format")
            return jsonify({'error': 'Invalid file format, CSV required'}), 400

        real_time_content = real_time_file.read().decode('utf-8')
        historical_content = historical_file.read().decode('utf-8')
        logger.info("Files decoded successfully")

        real_time_df = pd.read_csv(StringIO(real_time_content))
        historical_df = pd.read_csv(StringIO(historical_content))
        logger.info(f"Real-time rows: {len(real_time_df)}, Historical rows: {len(historical_df)}")

        results, error = reconcile_ihub_data(real_time_df, historical_df)
        if error:
            return jsonify(error), 400

        logger.info("IHub Processing completed successfully")
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in /reconcile: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error processing CSVs: {str(e)}'}), 500

# Catalyst Reconciliation endpoint
@app.route('/reconcile-catalyst', methods=['POST'])
def reconcile_catalyst():
    logger.info("Received request to /reconcile-catalyst")
    try:
        if 'realTimeData' not in request.files or 'historicalData' not in request.files:
            logger.error("Missing required files in request")
            return jsonify({'error': 'Both RealTime_Catalyst.csv and Historical_Catalyst.csv are required'}), 400

        real_time_file = request.files['realTimeData']
        historical_file = request.files['historicalData']
        logger.info(f"Files received: {real_time_file.filename}, {historical_file.filename}")

        if not real_time_file.filename.endswith('.csv') or not historical_file.filename.endswith('.csv'):
            logger.error("Invalid file format")
            return jsonify({'error': 'Invalid file format, CSV required'}), 400

        real_time_content = real_time_file.read().decode('utf-8')
        historical_content = historical_file.read().decode('utf-8')
        logger.info("Files decoded successfully")

        real_time_df = pd.read_csv(StringIO(real_time_content))
        historical_df = pd.read_csv(StringIO(historical_content))
        logger.info(f"Real-time rows: {len(real_time_df)}, Historical rows: {len(historical_df)}")

        results, error = reconcile_catalyst_data(real_time_df, historical_df)
        if error:
            return jsonify(error), 400

        logger.info("Catalyst Processing completed successfully")
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in /reconcile-catalyst: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error processing CSVs: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
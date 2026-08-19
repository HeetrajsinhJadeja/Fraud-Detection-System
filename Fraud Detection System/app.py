from flask import Flask, render_template, request, jsonify, redirect, url_for
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

app = Flask(__name__)

# Load the XGBoost model
try:
    with open('UI\fraud_detection_xgboost.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Create a logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

LOG_FILE = 'logs/transaction_logs.json'

# Initialize log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

def get_logs():
    try:
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def save_log(log_entry):
    logs = get_logs()
    logs.append(log_entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/api/check_transaction', methods=['POST'])
def check_transaction():
    try:
        # Get form data
        data = request.form.to_dict()
        
        # Convert string values to appropriate types
        features = {
            'step': int(data.get('step', 0)),
            'type': data.get('type', 'PAYMENT'),
            'amount': float(data.get('amount', 0)),
            'nameOrig': data.get('nameOrig', ''),
            'oldbalanceOrg': float(data.get('oldbalanceOrg', 0)),
            'newbalanceOrg': float(data.get('newbalanceOrg', 0)),
            'nameDest': data.get('nameDest', ''),
            'oldbalanceDest': float(data.get('oldbalanceDest', 0)),
            'newbalanceDest': float(data.get('newbalanceDest', 0))
        }
        
        # Prepare features for model
        # Convert 'type' to one-hot encoding
        transaction_types = ['PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT', 'CASH_IN']
        for t_type in transaction_types:
            features[f'type_{t_type}'] = 1 if features['type'] == t_type else 0
        
        # Create additional features that might be useful
        features['errorBalanceOrig'] = features['newbalanceOrg'] + features['amount'] - features['oldbalanceOrg']
        features['errorBalanceDest'] = features['oldbalanceDest'] + features['amount'] - features['newbalanceDest']
        
        # Add merchant/client indicator
        features['is_dest_merchant'] = 1 if features['nameDest'].startswith('M') else 0
        features['is_orig_merchant'] = 1 if features['nameOrig'].startswith('M') else 0
        
        # Create feature array for the model
        # Remove original 'type' and other non-numeric features
        model_features = {k: v for k, v in features.items() if k not in ['type', 'nameOrig', 'nameDest']}
        
        # Convert to DataFrame with specific ordering (adjust based on your model's expected features)
        feature_df = pd.DataFrame([model_features])
        
        # Use the model to predict
        # If model is not loaded, use the simple rules from your HTML
        if model is not None:
            # Get prediction
            prediction = model.predict_proba(feature_df)
            is_fraud = prediction[0][1] > 0.5  # Assuming index 1 is the fraud probability
            fraud_probability = prediction[0][1]
        else:
            # Fallback logic similar to your static test logic in the HTML
            type_val = features['type']
            amount = features['amount']
            nameOrig = features['nameOrig']
            nameDest = features['nameDest']
            
            is_fraud = False
            fraud_probability = 0.05
            
            if type_val == 'TRANSFER' and amount > 8000:
                is_fraud = True
                fraud_probability = 0.92
            elif type_val == 'CASH_OUT' and amount > 5000:
                is_fraud = True
                fraud_probability = 0.78
            elif amount > 3000 and nameOrig.startswith('C') and nameDest.startswith('C'):
                is_fraud = True
                fraud_probability = 0.65
        
        # Create response
        response = {
            'is_fraud': bool(is_fraud),
            'fraud_probability': float(fraud_probability),
            'transaction_details': {
                'type': features['type'],
                'amount': features['amount'],
                'origin_account': features['nameOrig'],
                'destination_account': features['nameDest']
            }
        }
        
        # Log the transaction
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': features['type'],
            'amount': features['amount'],
            'nameOrig': features['nameOrig'],
            'nameDest': features['nameDest'],
            'isFraud': bool(is_fraud),
            'probability': float(fraud_probability)
        }
        save_log(log_entry)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transaction_logs', methods=['GET'])
def get_transaction_logs():
    logs = get_logs()
    return jsonify(logs)

@app.route('/api/clear_logs', methods=['POST'])
def clear_logs():
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
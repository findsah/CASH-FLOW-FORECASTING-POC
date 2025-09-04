from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import yfinance as yf
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
CORS(app)

# Set up upload directory in user's local app data
if os.name == 'nt':  # Windows
    UPLOAD_FOLDER = os.path.join(os.environ['LOCALAPPDATA'], 'CashFlowForecaster', 'uploads')
else:  # Unix/Linux/Mac
    UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), '.local', 'share', 'CashFlowForecaster', 'uploads')

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Sample investment opportunities
INVESTMENT_OPPORTUNITIES = {
    'stocks': ['VOO', 'QQQ', 'VTI'],
    'bonds': ['BND', 'TLT', 'AGG'],
    'reits': ['VNQ', 'SCHH', 'O'],
    'crypto': ['BTC-USD', 'ETH-USD', 'ADA-USD']
}

def analyze_cash_flow(df):
    # Basic analysis of cash flow data
    analysis = {
        'total_income': df[df['amount'] > 0]['amount'].sum(),
        'total_expenses': abs(df[df['amount'] < 0]['amount'].sum()),
        'net_cash_flow': df['amount'].sum(),
        'monthly_avg_income': df[df['amount'] > 0].groupby(df['date'].dt.to_period('M'))['amount'].sum().mean(),
        'monthly_avg_expenses': abs(df[df['amount'] < 0].groupby(df['date'].dt.to_period('M'))['amount'].sum().mean())
    }
    return analysis

def forecast_cash_flow(df, months=6):
    # Simple forecasting using moving average
    monthly_data = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()
    forecast = monthly_data.rolling(window=3, min_periods=1).mean().iloc[-1]
    
    forecast_dates = pd.date_range(
        start=df['date'].max() + pd.offsets.MonthBegin(1),
        periods=months,
        freq='M'
    )
    
    forecast_values = [forecast] * months
    
    return forecast_dates, forecast_values

def get_investment_suggestions(risk_profile='moderate'):
    suggestions = {
        'conservative': {
            'stocks': 30,
            'bonds': 50,
            'reits': 10,
            'crypto': 10,
            'description': 'Lower risk, stable returns'
        },
        'moderate': {
            'stocks': 50,
            'bonds': 30,
            'reits': 10,
            'crypto': 10,
            'description': 'Balanced risk and return'
        },
        'aggressive': {
            'stocks': 60,
            'bonds': 10,
            'reits': 10,
            'crypto': 20,
            'description': 'Higher risk, potential for higher returns'
        }
    }
    
    return suggestions.get(risk_profile.lower(), suggestions['moderate'])

from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file:
            # Create a secure filename and save to local storage
            from werkzeug.utils import secure_filename
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Save the file
            file.save(save_path)
            
            # Process the file based on its type
            try:
                if filename.lower().endswith('.csv'):
                    df = pd.read_csv(save_path)
                    # Convert date column if needed
                    if 'date' in df.columns:
                        df['date'] = pd.to_datetime(df['date'])
                    
                    # Basic analysis
                    analysis = analyze_cash_flow(df)
                    forecast_dates, forecast_values = forecast_cash_flow(df)
                    
                    # Get investment suggestions
                    suggestions = get_investment_suggestions()
                    
                    return jsonify({
                        'status': 'success',
                        'file_path': save_path,
                        'analysis': analysis,
                        'forecast': {
                            'dates': [str(d) for d in forecast_dates],
                            'values': forecast_values
                        },
                        'investment_suggestions': suggestions
                    })
                    
            except Exception as e:
                import traceback
                return jsonify({
                    'error': 'Error processing file',
                    'details': str(e),
                    'traceback': traceback.format_exc()
                }), 500
        
        return jsonify({'error': 'File processing failed'}), 500
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': 'Server error',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/get_stock_data')
def get_stock_data():
    symbol = request.args.get('symbol', 'VOO')
    period = request.args.get('period', '1y')
    
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        return jsonify({
            'dates': hist.index.strftime('%Y-%m-%d').tolist(),
            'prices': hist['Close'].values.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

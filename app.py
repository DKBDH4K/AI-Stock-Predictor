from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from yahooquery import Ticker
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from keras.models import load_model, Sequential
from keras.layers import LSTM, Dense
import os
import datetime
import threading

app = Flask(__name__)

# ====== GLOBALS & CACHING ======
model = None
# Cache to store fetched DataFrames (key: ticker_date)
data_cache = {}
# Cache to store trained RF models (key: ticker)
rf_cache = {}
cache_lock = threading.Lock()

def get_model():
    global model
    if model is not None:
        return model
        
    try:
        model = load_model('keras_model.h5')
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Standard model loading failed: {str(e)}")
        try:
            model = load_model('keras_model.h5', compile=False, custom_objects={'LSTM': LSTM})
            print("Model loaded with custom LSTM configuration!")
        except Exception as e:
            print(f"Custom loading failed: {str(e)}")
            try:
                model = Sequential([
                    LSTM(units=50, return_sequences=True, input_shape=(100, 1)),
                    LSTM(units=50, return_sequences=False),
                    Dense(units=25),
                    Dense(units=1)
                ])
                model.load_weights('keras_model.h5')
                print("Successfully loaded weights into recreated architecture!")
            except Exception as e:
                print(f"Final loading attempt failed: {str(e)}")
                return None
    return model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data or 'ticker' not in data:
            return jsonify({'error': 'No ticker provided.'}), 400
            
        ticker = str(data.get('ticker', 'AAPL')).strip().upper()
        
        # 1. Ensure Keras Model is loaded
        lstm_model = get_model()
        if lstm_model is None:
            return jsonify({'error': 'Failed to load the prediction model. Please check the server logs.'}), 500

        end_date = datetime.date.today().strftime('%Y-%m-%d')
        cache_key = f"{ticker}_{end_date}"
        
        # 2. Fetch or Load Data from Cache
        with cache_lock:
            if cache_key in data_cache:
                df = data_cache[cache_key].copy()
            else:
                try:
                    t = Ticker(ticker)
                    df = t.history(start='2012-01-01', end=end_date)
                except Exception as e:
                    return jsonify({'error': f'Network error fetching data for {ticker}: {str(e)}'}), 502
                
                if df.empty or isinstance(df, dict):
                    return jsonify({'error': f'No historical data found for {ticker}.'}), 404
                    
                df = df.reset_index()
                if 'date' in df.columns:
                    df.set_index('date', inplace=True)
                df.index = pd.to_datetime(df.index)
                df.sort_index(inplace=True)
                data_cache[cache_key] = df.copy()
            
        # 3. Preprocessing
        if 'close' not in df.columns:
            return jsonify({'error': 'Close price data not found for this ticker.'}), 500
            
        close_data = df[['close']]
        dataset = close_data.values
        
        if len(dataset) < 150:
            return jsonify({'error': 'Not enough historical data to generate predictions (minimum 150 days required).'}), 400
            
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(dataset)

        training_size = int(len(scaled_data) * 0.7)
        train_data = scaled_data[0:training_size, :]
        test_data = scaled_data[training_size - 100:, :]
        
        # 4. Prepare Test Data
        x_test = []
        y_test = dataset[training_size:]
        for i in range(100, len(test_data)):
            x_test.append(test_data[i-100:i, 0])
        
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        # 5. Train or Load Random Forest
        with cache_lock:
            if ticker in rf_cache:
                rf_model = rf_cache[ticker]
            else:
                x_train = []
                y_train = []
                for i in range(100, len(train_data)):
                    x_train.append(train_data[i-100:i, 0])
                    y_train.append(train_data[i, 0])
                    
                x_train, y_train = np.array(x_train), np.array(y_train)
                
                # Optimized RF parameters for speed and decent accuracy
                rf_model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
                rf_model.fit(x_train, y_train)
                rf_cache[ticker] = rf_model

        # 6. Make Predictions
        lstm_predictions = lstm_model.predict(x_test, verbose=0)
        lstm_predictions = scaler.inverse_transform(lstm_predictions)
        
        rf_x_test = x_test.reshape((x_test.shape[0], x_test.shape[1]))
        rf_predictions = rf_model.predict(rf_x_test)
        rf_predictions = rf_predictions.reshape(-1, 1)
        rf_predictions = scaler.inverse_transform(rf_predictions)
        
        predictions = (lstm_predictions + rf_predictions) / 2.0
        
        # 7. Calculate Metrics & Formats
        rmse = np.sqrt(np.mean((predictions - y_test)**2))
        
        dates = df.index.strftime('%Y-%m-%d').tolist()
        historical_prices = dataset.flatten().tolist()
        
        test_dates = df.index[training_size:].strftime('%Y-%m-%d').tolist()
        predicted_prices = predictions.flatten().tolist()
        actual_test_prices = y_test.flatten().tolist()
        
        # Generate full-range predictions for analytics
        x_all = []
        for i in range(100, len(scaled_data)):
            x_all.append(scaled_data[i-100:i, 0])
        x_all = np.array(x_all)
        x_all = np.reshape(x_all, (x_all.shape[0], x_all.shape[1], 1))
        
        lstm_all_predictions = lstm_model.predict(x_all, verbose=0)
        lstm_all_predictions = scaler.inverse_transform(lstm_all_predictions)
        
        rf_x_all = x_all.reshape((x_all.shape[0], x_all.shape[1]))
        rf_all_predictions = rf_model.predict(rf_x_all)
        rf_all_predictions = rf_all_predictions.reshape(-1, 1)
        rf_all_predictions = scaler.inverse_transform(rf_all_predictions)
        
        all_predictions = (lstm_all_predictions + rf_all_predictions) / 2.0
        
        analysis_df = pd.DataFrame(index=df.index[100:])
        analysis_df['Actual'] = dataset[100:].flatten()
        analysis_df['Predicted'] = all_predictions.flatten()
        
        def calculate_accuracy(actual, predicted):
            if actual == 0: return 0
            return max(0, 100 - (abs(actual - predicted) / actual) * 100)
            
        analysis_df['Year'] = analysis_df.index.year
        yearly_df = analysis_df.groupby('Year').mean().tail(5)
        yearly_data = [{'period': str(year), 'actual': float(row['Actual']), 'predicted': float(row['Predicted']), 'accuracy': float(calculate_accuracy(row['Actual'], row['Predicted']))} for year, row in yearly_df.iterrows()]
            
        analysis_df['Month_Year'] = analysis_df.index.to_period('M')
        monthly_df = analysis_df.groupby('Month_Year').mean().tail(12)
        monthly_data = [{'period': str(period), 'actual': float(row['Actual']), 'predicted': float(row['Predicted']), 'accuracy': float(calculate_accuracy(row['Actual'], row['Predicted']))} for period, row in monthly_df.iterrows()]
        
        actuals = analysis_df['Actual'].values
        predicteds = analysis_df['Predicted'].values
        valid_idx = actuals != 0
        total_accuracy = float(np.mean(np.maximum(0, 100 - (np.abs(actuals[valid_idx] - predicteds[valid_idx]) / actuals[valid_idx]) * 100))) if np.any(valid_idx) else 0.0
            
        return jsonify({
            'success': True,
            'ticker': ticker,
            'dates': dates,
            'historical_prices': historical_prices,
            'test_dates': test_dates,
            'predicted_prices': predicted_prices,
            'actual_test_prices': actual_test_prices,
            'rmse': float(rmse),
            'total_accuracy': total_accuracy,
            'yearly_data': yearly_data,
            'monthly_data': monthly_data
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    get_model()
    app.run(debug=True, port=5000)
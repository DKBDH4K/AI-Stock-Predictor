import pandas as pd
import numpy as np
from yahooquery import Ticker
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import EarlyStopping
import random

# A diverse mix of top Indian stocks from different sectors to build a robust, generalized model
tickers = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ITC.NS', 'LT.NS', 'SBIN.NS', 'BHARTIARTL.NS']

x_train_all = []
y_train_all = []

print(f"Fetching historical data for {len(tickers)} diverse tickers (2012-2024)...")

for ticker_symbol in tickers:
    print(f"Processing {ticker_symbol}...")
    try:
        t = Ticker(ticker_symbol)
        df = t.history(start='2012-01-01', end='2024-01-01')
        
        if df.empty or isinstance(df, dict):
            print(f"Skipping {ticker_symbol} - No data.")
            continue
            
        df = df.reset_index()
        if 'date' in df.columns:
            df.set_index('date', inplace=True)
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)

        if 'close' not in df.columns:
            continue
            
        data = df.filter(['close'])
        dataset = data.values
        
        # Scale each stock individually so the model learns shapes/patterns rather than absolute prices
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(dataset)

        # Use 85% of data from each stock
        training_data_len = int(np.ceil( len(dataset) * .85 )) 
        train_data = scaled_data[0:int(training_data_len), :]

        for i in range(100, len(train_data)):
            x_train_all.append(train_data[i-100:i, 0])
            y_train_all.append(train_data[i, 0])
            
    except Exception as e:
        print(f"Error processing {ticker_symbol}: {e}")

# Convert to numpy arrays
x_train_all = np.array(x_train_all)
y_train_all = np.array(y_train_all)

# Reshape for LSTM [samples, time steps, features]
x_train_all = np.reshape(x_train_all, (x_train_all.shape[0], x_train_all.shape[1], 1))

print(f"\nTotal training samples across all tickers: {x_train_all.shape[0]}")

# Shuffle the aggregated dataset to prevent the model from memorizing specific stock sequences sequentially
print("Shuffling dataset...")
indices = np.arange(x_train_all.shape[0])
np.random.shuffle(indices)
x_train_all = x_train_all[indices]
y_train_all = y_train_all[indices]

print("\nBuilding generalized optimized LSTM model...")
model = Sequential()
# Layer 1
model.add(LSTM(units=128, return_sequences=True, input_shape=(x_train_all.shape[1], 1)))
model.add(Dropout(0.2)) # Prevent overfitting
# Layer 2
model.add(LSTM(units=64, return_sequences=True))
model.add(Dropout(0.2))
# Layer 3
model.add(LSTM(units=64, return_sequences=False))
model.add(Dropout(0.2))
# Dense Layers
model.add(Dense(units=25))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')

# Early stopping to prevent over-training
early_stop = EarlyStopping(monitor='loss', patience=4, restore_best_weights=True)

print("Starting training... This will take a while depending on your CPU/GPU.")
model.fit(x_train_all, y_train_all, batch_size=64, epochs=30, callbacks=[early_stop])

model.save('keras_model.h5')
print("\nGlobal generalized model successfully trained and saved as 'keras_model.h5'!")

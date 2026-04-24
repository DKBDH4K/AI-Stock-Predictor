import pandas as pd
import numpy as np
from yahooquery import Ticker
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint

print("Fetching historical data for training (AAPL 2012-2024)...")
t = Ticker('AAPL')
df = t.history(start='2012-01-01', end='2024-01-01')
df = df.reset_index()
df.set_index('date', inplace=True)
df.index = pd.to_datetime(df.index)
df.sort_index(inplace=True)

data = df.filter(['close'])
dataset = data.values
training_data_len = int(np.ceil( len(dataset) * .8 )) # Increased training size to 80%

print(f"Scaling {len(dataset)} records...")
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

train_data = scaled_data[0:int(training_data_len), :]
x_train = []
y_train = []

for i in range(100, len(train_data)):
    x_train.append(train_data[i-100:i, 0])
    y_train.append(train_data[i, 0])
    
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

print("Building optimized LSTM model...")
model = Sequential()
# Layer 1
model.add(LSTM(units=128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
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
model.summary()

# Early stopping to find the best epoch automatically
early_stop = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)

print("Starting training... This may take a few minutes.")
model.fit(x_train, y_train, batch_size=32, epochs=50, callbacks=[early_stop])

model.save('keras_model.h5')
print("Optimized model successfully trained and saved as 'keras_model.h5'!")

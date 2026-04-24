# AI Stock Predictor 📈

An advanced, interactive web application that uses a powerful Ensemble Machine Learning model (LSTM Neural Network + Random Forest Regressor) to forecast stock prices. Built with a robust Flask backend and a modern, custom animated frontend.

## 🌟 Features
- **Accurate Ensemble Forecasting:** Combines a pre-trained Keras LSTM deep learning model with a dynamically trained Scikit-Learn Random Forest model. This ensemble approach significantly improves predictive accuracy by blending long-term sequential pattern recognition with non-linear decision tree logic.
- **Dynamic Data Scraping:** Uses the `yahooquery` API to bypass traditional rate limits and dynamically fetch up-to-date historical stock data on the fly.
- **Comprehensive Analytics:** Automatically calculates and displays the Root Mean Squared Error (RMSE), 5-year average performance, 12-month average performance, and total lifetime prediction accuracy.
- **Custom Interactive UI:** Features a completely custom HTML5 Canvas animated background with moving candlesticks and floating ticker symbols that react to your mouse movements, paired with beautiful typography (Michroma & Rajdhani fonts) and modern glassmorphism styling.
- **Alphabetized Selection:** Easily choose from a comprehensive, alphabetically sorted list of top Indian stocks.
- **Jupyter Notebook Integration:** Includes a clean `model_training.ipynb` file showcasing exactly how the initial data was gathered, preprocessed, and how the neural network was structured and trained.

## 🛠️ Technology Stack
- **Backend:** Python, Flask
- **Machine Learning:** Keras, TensorFlow, Scikit-Learn (Random Forest & Scalers)
- **Data Acquisition:** YahooQuery, Pandas, NumPy
- **Frontend:** HTML5 Canvas, CSS3, JavaScript, Chart.js

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3 installed. You will also need `pip` to install the required libraries.

### Installation
1. Clone this repository to your local machine.
2. Open your terminal and navigate to the project directory.
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. Start the local Flask web server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://127.0.0.1:5000/`.
3. Select an Indian stock from the dropdown menu and click **Predict** to view the historical performance and AI forecasts!

## 🧠 How the Model Works
The prediction pipeline uses an Ensemble approach:
1. **LSTM (Long Short-Term Memory):** The neural network uses a 100-day "lookback" window to evaluate sequential historical closing prices. The provided `keras_model.h5` contains the optimized, globally trained weights for the network.
2. **Random Forest:** When a user selects a specific stock, a new Random Forest Regressor is dynamically trained in the backend specifically on that stock's historical data to capture immediate price action boundaries.
3. **Ensemble Averaging:** The predictions from both models are averaged together to output a highly robust and accurate final price prediction.

## ⚠️ Disclaimer
This application is designed for educational and informational purposes only. It is not financial advice. The stock market is highly volatile and unpredictable. Always do your own research before making real-world investment decisions.

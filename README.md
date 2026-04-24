# AI Stock Predictor 📈

An advanced, interactive web application that uses a Long Short-Term Memory (LSTM) Neural Network to forecast stock prices. Built with a robust Flask backend and a modern, glassmorphism-styled animated frontend.

## 🌟 Features
- **Accurate Market Forecasting:** Utilizes an LSTM deep learning model built with Keras and TensorFlow to identify temporal patterns in financial data.
- **Dynamic Data Scraping:** Uses the `yahooquery` API to bypass traditional rate limits and dynamically fetch up-to-date historical stock data.
- **Comprehensive Analytics:** Automatically calculates and displays the Root Mean Squared Error (RMSE), 5-year average performance, 12-month average performance, and total lifetime prediction accuracy.
- **Stunning UI:** Features a highly interactive animated background (Vanta.js), beautiful responsive charts (Chart.js), and modern glassmorphism styling.
- **Jupyter Notebook Integration:** Includes a clean `model_training.ipynb` file showcasing exactly how the data was gathered, preprocessed, and how the neural network was structured and trained.

## 🛠️ Technology Stack
- **Backend:** Python, Flask
- **Machine Learning:** Keras, TensorFlow, Scikit-Learn
- **Data Acquisition:** YahooQuery, Pandas, NumPy
- **Frontend:** HTML5, CSS3, JavaScript, Chart.js, Vanta.js (Three.js)

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
The LSTM (Long Short-Term Memory) model uses a 100-day "lookback" window. This means it evaluates the closing prices of the previous 100 trading days to predict the price on the 101st day. The provided `keras_model.h5` contains the optimized, trained weights for the network.

## ⚠️ Disclaimer
This application is designed for educational and informational purposes only. It is not financial advice. The stock market is highly volatile and unpredictable. Always do your own research before making real-world investment decisions.

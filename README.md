# AI Stock Predictor 📈

AI Stock Predictor is an advanced, interactive web application that uses a powerful Ensemble Machine Learning model (LSTM Neural Network + Random Forest Regressor) to forecast stock prices. Built with a robust Flask backend and a modern, custom animated frontend.

By combining long-term sequential pattern recognition with non-linear decision tree logic, AI Stock Predictor performs reliably and accurately for forecasting stock price trends.

## 🚀 Key Features
**Accurate Ensemble Forecasting:** Combines a pre-trained Keras LSTM deep learning model with a dynamically trained Scikit-Learn Random Forest model. This ensemble approach significantly improves predictive accuracy by blending long-term sequential pattern recognition with non-linear decision tree logic.
**Dynamic Data Scraping:** Uses the `yahooquery` API to bypass traditional rate limits and dynamically fetch up-to-date historical stock data on the fly.
**Comprehensive Analytics:** Automatically calculates and displays the Root Mean Squared Error (RMSE), 5-year average performance, 12-month average performance, and total lifetime prediction accuracy.
**Custom Interactive UI:** Features a completely custom HTML5 Canvas animated background with moving candlesticks and floating ticker symbols that react to your mouse movements, paired with beautiful typography (Michroma & Rajdhani fonts) and modern glassmorphism styling.
**Alphabetized Selection:** Easily choose from a comprehensive, alphabetically sorted list of top Indian stocks.

## 🛠️ Technology Stack
**Backend:** Python 3, Flask
**Machine Learning Models:**
- Keras, TensorFlow (`keras_model.h5`)
- Scikit-Learn (Random Forest & Scalers)
**Data Acquisition:** YahooQuery, Pandas, NumPy
**Frontend:** HTML5 Canvas, CSS3, JavaScript, Chart.js

## 📁 Project Structure
AI Stock Predictor/
├── app.py                 # Core Flask application backend
├── sort_options.py        # Alphabetized Indian stock list
├── keras_model.h5         # Pre-trained LSTM Neural Network weights
├── model_training.ipynb   # Jupyter Notebook showing data gathering, preprocessing, and model training
├── requirements.txt       # Python dependency list
├── static/                # CSS/JS and static assets
│   └── style.css          # Custom styling and glassmorphism UI
└── templates/             # HTML templates 
    └── index.html         # Main dashboard and landing page

## ⚙️ Setup and Installation
Clone the Repository and navigate to the project root.
Install Dependencies:
Make sure you have Python 3 installed. You will also need pip to install the required libraries.
```bash
pip install -r requirements.txt
```

## ▶️ Running the Application
Start the local Flask web server:
```bash
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```
**Note on Selection:** Select an Indian stock from the dropdown menu and click **Predict** to view the historical performance and AI forecasts!

## 🧠 How it Works
**LSTM (Long Short-Term Memory):** The neural network uses a 100-day "lookback" window to evaluate sequential historical closing prices. The provided `keras_model.h5` contains the optimized, globally trained weights for the network.
**Random Forest:** When a user selects a specific stock, a new Random Forest Regressor is dynamically trained in the backend specifically on that stock's historical data to capture immediate price action boundaries.
**Ensemble Averaging:** The predictions from both models are averaged together to output a highly robust and accurate final price prediction.

## ⚠️ Disclaimer
This application is designed for educational and informational purposes only. It is not financial advice. The stock market is highly volatile and unpredictable. Always do your own research before making real-world investment decisions.

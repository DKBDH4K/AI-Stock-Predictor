# 📈 AI Stock Predictor: Advanced Forecasting System

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Framework](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
![Machine Learning](https://img.shields.io/badge/keras-LSTM-%23D00000.svg?style=flat&logo=Keras&logoColor=white)
![Ensemble](https://img.shields.io/badge/sklearn-Random_Forest-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**AI Stock Predictor** is a state-of-the-art, interactive web application that leverages an **Ensemble Machine Learning Architecture** (LSTM Neural Network + Random Forest Regressor) to forecast stock prices with high accuracy. The application features a robust Flask backend with intelligent caching, paired with a visually stunning, custom-animated glassmorphism frontend.

By blending the deep sequential pattern recognition of LSTMs with the non-linear decision tree logic of Random Forests, this platform provides reliable trend forecasting for over 100 top Indian stocks.

---

## ✨ Key Features & Enhancements

- **🧠 Advanced Ensemble Forecasting:** A pre-trained deep learning Keras LSTM model combined with a dynamically trained Scikit-Learn Random Forest model. 
- **⚡ High-Performance Architecture:** Implements thread-safe caching mechanisms for both YahooQuery financial data and Random Forest models, drastically reducing load times and redundant network calls.
- **🌐 Dynamic Live Data:** Uses the `yahooquery` API to bypass traditional rate limits, fetching the latest market data on the fly.
- **📊 Comprehensive Analytics:** Automatically calculates RMSE, 5-year average performance, 12-month average performance, and total lifetime prediction accuracy.
- **🎨 Premium UI/UX:** A stunning HTML5 Canvas animated background with moving candlesticks, floating ticker symbols that react to mouse movements, premium typography, and dynamic Chart.js visualizations.
- **🛡️ Robust Error Handling:** Graceful fallback mechanisms for model loading, network timeouts, and data validation to ensure uninterrupted user experience.

---

## 🛠️ Technology Stack

**Backend Architecture:**
- Python 3.8+
- Flask (Web Server)
- Threading & Caching (Performance Optimization)

**Machine Learning Pipeline:**
- Keras & TensorFlow (`keras_model.h5`)
- Scikit-Learn (Random Forest Regressors, MinMax Scalers)
- Pandas & NumPy (Data Processing)

**Frontend Design:**
- HTML5 Canvas & CSS3 (Glassmorphism & Micro-animations)
- Vanilla JavaScript (Interactive elements)
- Chart.js (Data Visualization)

---

## 📁 Project Structure

```text
AI-Stock-Predictor/
├── app.py                 # Core Flask backend with caching & error handling
├── sort_options.py        # Utilities for stock options
├── keras_model.h5         # Pre-trained LSTM Neural Network weights
├── model_training.ipynb   # Jupyter Notebook: Data gathering & LSTM training
├── requirements.txt       # Project dependencies
├── static/                
│   ├── style.css          # Advanced glassmorphism & UI animations
│   └── script.js          # Interactive canvas, charts, and AJAX logic
└── templates/             
    └── index.html         # Main application dashboard
```

---

## ⚙️ Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/deioncolaco28/AI-Stock-Predictor.git
   cd AI-Stock-Predictor
   ```

2. **Install Dependencies:**
   Ensure Python 3.8+ is installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```

4. **Access the Dashboard:**
   Open your browser and navigate to `http://127.0.0.1:5000/`. Select an Indian stock from the dropdown and click **Predict**.

---

## 🧠 Under the Hood

1. **LSTM (Long Short-Term Memory):** Uses a 100-day sliding window to evaluate historical closing prices, identifying long-term sequential patterns using optimized, pre-trained weights.
2. **Random Forest Regressor:** A secondary model trained on-the-fly specifically for the selected ticker to capture immediate price boundaries and local volatility. (Now cached for speed!)
3. **Ensemble Averaging:** The outputs from both models are merged to produce a robust final prediction, minimizing the individual weaknesses of both architectures.

---

## ⚠️ Disclaimer

This application is strictly for **educational and informational purposes only**. It does not constitute financial advice. The stock market is highly volatile, and AI predictions should not be solely relied upon for real-world investments. Always conduct your own research.

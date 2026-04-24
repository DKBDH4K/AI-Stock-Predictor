// Initialize Vanta.js Background
document.addEventListener('DOMContentLoaded', () => {
    VANTA.NET({
        el: "#vanta-bg",
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        color: 0x00ffcc,
        backgroundColor: 0x0f172a,
        points: 12.00,
        maxDistance: 22.00,
        spacing: 18.00
    });
});

// Chart Instances
let histChart = null;
let predChart = null;

// Handle Form Submission
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const ticker = document.getElementById('ticker-input').value.trim();
    const btn = document.getElementById('predict-btn');
    const btnText = btn.querySelector('.btn-text');
    const spinner = btn.querySelector('.spinner');
    const errorMsg = document.getElementById('error-message');
    const resultsSection = document.getElementById('results-section');
    
    if (!ticker) return;

    // UI Loading State
    btn.disabled = true;
    btnText.classList.add('hidden');
    spinner.classList.remove('hidden');
    errorMsg.classList.add('hidden');
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ticker: ticker })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch prediction');
        }
        
        // Update Stats
        document.getElementById('rmse-value').innerText = data.rmse.toFixed(2);
        document.getElementById('ticker-display').innerText = data.ticker.toUpperCase();
        document.getElementById('accuracy-value').innerText = data.total_accuracy.toFixed(2) + '%';
        
        // Show Results
        resultsSection.classList.remove('hidden');
        
        // Render Charts
        renderHistoricalChart(data.dates, data.historical_prices, data.ticker);
        renderPredictionChart(data.test_dates, data.actual_test_prices, data.predicted_prices, data.ticker);
        
        // Render Tables
        renderDataTables(data.yearly_data, data.monthly_data);
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (err) {
        errorMsg.innerText = err.message;
        errorMsg.classList.remove('hidden');
        resultsSection.classList.add('hidden');
    } finally {
        // Reset UI
        btn.disabled = false;
        btnText.classList.remove('hidden');
        spinner.classList.add('hidden');
    }
});

// Chart.js Default Config for Dark Theme
Chart.defaults.color = '#a0aab2';
Chart.defaults.font.family = "'Outfit', sans-serif";

function renderHistoricalChart(dates, prices, ticker) {
    const ctx = document.getElementById('historicalChart').getContext('2d');
    
    if (histChart) {
        histChart.destroy();
    }

    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(0, 255, 204, 0.5)');
    gradient.addColorStop(1, 'rgba(0, 255, 204, 0.0)');

    histChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: `${ticker.toUpperCase()} Closing Price`,
                data: prices,
                borderColor: '#00ffcc',
                backgroundColor: gradient,
                borderWidth: 2,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 6,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#00ffcc',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1
                }
            },
            scales: {
                x: { 
                    grid: { display: false, drawBorder: false },
                    ticks: { maxTicksLimit: 8 }
                },
                y: { 
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

function renderPredictionChart(dates, actual, predicted, ticker) {
    const ctx = document.getElementById('predictionChart').getContext('2d');
    
    if (predChart) {
        predChart.destroy();
    }

    predChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Actual Price',
                    data: actual,
                    borderColor: '#ffffff',
                    borderWidth: 2,
                    fill: false,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    tension: 0.1
                },
                {
                    label: 'Predicted Price',
                    data: predicted,
                    borderColor: '#7000ff',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { color: '#fff', usePointStyle: true }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1
                }
            },
            scales: {
                x: { 
                    grid: { display: false, drawBorder: false },
                    ticks: { maxTicksLimit: 8 }
                },
                y: { 
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

function renderDataTables(yearlyData, monthlyData) {
    const yearlyTableBody = document.querySelector('#yearly-table tbody');
    const monthlyTableBody = document.querySelector('#monthly-table tbody');
    
    yearlyTableBody.innerHTML = '';
    monthlyTableBody.innerHTML = '';

    if (yearlyData) {
        yearlyData.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.period}</td>
                <td>₹${row.actual.toFixed(2)}</td>
                <td>₹${row.predicted.toFixed(2)}</td>
                <td class="${row.accuracy > 90 ? 'text-success' : 'text-warning'}">${row.accuracy.toFixed(2)}%</td>
            `;
            yearlyTableBody.appendChild(tr);
        });
    }

    if (monthlyData) {
        monthlyData.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.period}</td>
                <td>₹${row.actual.toFixed(2)}</td>
                <td>₹${row.predicted.toFixed(2)}</td>
                <td class="${row.accuracy > 90 ? 'text-success' : 'text-warning'}">${row.accuracy.toFixed(2)}%</td>
            `;
            monthlyTableBody.appendChild(tr);
        });
    }
}

class FraudDetectionDashboard {
    constructor() {
        this.apiBase = window.location.origin;
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkHealth();
        this.setCurrentTimestamp();
    }

    bindEvents() {
        // Prediction form
        const predictionForm = document.getElementById('predictionForm');
        if (predictionForm) {
            predictionForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.predictFraud();
            });
        }

        // Health check button
        const healthBtn = document.querySelector('button[onclick="dashboard.checkHealth()"]');
        if (healthBtn) {
            healthBtn.addEventListener('click', () => {
                this.checkHealth();
            });
        }

        // Quick test buttons
        document.querySelectorAll('.quick-test button').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const amount = e.target.textContent.match(/\$([0-9.]+)/)[1];
                this.testTransaction(parseFloat(amount));
            });
        });
    }

    setCurrentTimestamp() {
        const now = new Date();
        const localDateTime = now.toISOString().slice(0, 16);
        const timestampInput = document.getElementById('timestamp');
        if (timestampInput) {
            timestampInput.value = localDateTime;
        }
    }

    async predictFraud() {
        const transactionId = document.getElementById('transaction_id').value;
        const amount = parseFloat(document.getElementById('amount').value);
        const timestamp = document.getElementById('timestamp').value;

        const transaction = {
            transaction_id: transactionId || `TX_${Date.now()}`,
            amount: amount,
            timestamp: timestamp,
            merchant_id: "WEB_DASHBOARD",
            customer_id: "DASHBOARD_USER",
            location: "online",
            country: "US"
        };

        this.showLoading();

        try {
            const response = await fetch(`${this.apiBase}/api/v1/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(transaction)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.displayResult(result);
        } catch (error) {
            this.displayError(error.message);
        }
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.apiBase}/api/v1/health`);
            const health = await response.json();
            
            const statusDiv = document.getElementById('healthStatus');
            if (statusDiv) {
                statusDiv.className = `status ${health.status}`;
                statusDiv.innerHTML = `
                    Status: <strong>${health.status.toUpperCase()}</strong><br>
                    ML Model: ${health.model_loaded ? '✅' : '❌'}<br>
                    Last Check: ${new Date().toLocaleString()}
                `;
            }
        } catch (error) {
            const statusDiv = document.getElementById('healthStatus');
            if (statusDiv) {
                statusDiv.className = 'status unhealthy';
                statusDiv.innerHTML = `Status: <strong>UNREACHABLE</strong><br>Error: ${error.message}`;
            }
        }
    }

    testTransaction(amount) {
        document.getElementById('amount').value = amount;
        document.getElementById('transaction_id').value = `TEST_${Date.now()}`;
        this.setCurrentTimestamp();
        this.predictFraud();
    }

    showLoading() {
        const resultDiv = document.getElementById('result');
        if (resultDiv) {
            resultDiv.className = 'result';
            resultDiv.innerHTML = '<div style="text-align: center;">⏳ Analyzing transaction...</div>';
        }
    }

    displayResult(result) {
        const resultDiv = document.getElementById('result');
        if (!resultDiv) return;

        resultDiv.className = `result ${result.prediction ? 'fraud' : 'legitimate'}`;
        
        if (result.prediction) {
            resultDiv.innerHTML = `
                <h4>🚨 FRAUD DETECTED</h4>
                <p>Transaction: ${result.transaction_id}</p>
                <p>Risk: <strong>${result.risk_level.toUpperCase()}</strong></p>
                <p>Probability: <strong>${(result.probability * 100).toFixed(1)}%</strong></p>
            `;
        } else {
            resultDiv.innerHTML = `
                <h4>✅ LEGITIMATE</h4>
                <p>Transaction: ${result.transaction_id}</p>
                <p>Risk: <strong>${result.risk_level.toUpperCase()}</strong></p>
                <p>Probability: <strong>${(result.probability * 100).toFixed(1)}%</strong></p>
            `;
        }
    }

    displayError(message) {
        const resultDiv = document.getElementById('result');
        if (resultDiv) {
            resultDiv.className = 'result fraud';
            resultDiv.innerHTML = `
                <h4>❌ ERROR</h4>
                <p>${message}</p>
            `;
        }
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new FraudDetectionDashboard();
});
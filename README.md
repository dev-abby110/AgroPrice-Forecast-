# AgroPrice Forecast 🌾

An AI-powered agricultural commodity price prediction system with real-time forecasting and chat assistance.

## Features 🚀

- **Intelligent Price Prediction**: Advanced machine learning models for accurate price forecasting of agricultural commodities.
- **AI-Powered Assistant**: Multi-lingual chatbot for agricultural queries (English, Hindi, Marathi).
- **Interactive User Interface**: A modern, responsive interface featuring a sleek glassmorphism design.
- **Location-Specific Insights**: State, district, and market-based price predictions.
- **Comprehensive Commodity Coverage**: Supports multiple commodities and varieties for diverse agricultural needs.

## Tech Stack 🛠️

- **Frontend**: HTML5, CSS3, JavaScript, jQuery
- **Backend**: Python, Flask
- **Machine Learning Models**: 
  - Random Forest
  - XGBoost
  - Stacking Ensemble
- **AI Integration**: Groq API powered by LLaMa 3.3 70B model
- **Data Processing**: Pandas, NumPy
- **Visualization**: Custom CSS animations for interactive data representation

## Project Structure 📁

```
capstone/
├── data/
│   └── Price_Agriculture_commodities_Week.csv
├── models/
│   └── stacking_ensemble_model.pkl
├── static/
│   ├── images/
│   ├── script.js
│   └── styles.css
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
└── README.md
```

## 📸 Screenshots

#### 🔹 Home Page  
![Home Page](static/images/homepage.png)

#### 🔹 Price Prediction Page  
![Price Prediction](static/images/prediction_page.png)

#### 🔹 AI Chat Assistant  
![Chat Assistant](static/images/chat_assistant.png)

## Setup Instructions 🚀

### 1. Clone the Repository
```bash
git clone [repository-url]
cd capstone
```

### 2. Download Required Files
- **Dataset**: [Price_Agriculture_commodities_Week.csv](your-data-link) → Place in `data/` folder.
- **Trained Model**: [stacking_ensemble_model.pkl](your-model-link) → Place in `models/` folder.

### 3. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
- Create a `.env` file and add the following:
```
GROQ_API_KEY=your_api_key_here
```

### 6. Run the Application
```bash
python app.py
```

### 7. Access the Application
Visit: [http://localhost:5000](http://localhost:5000)

## Model Information 📊

### Model Architecture
- **Base Models**: Random Forest and XGBoost
- **Meta-Model**: Linear Regression for optimal stacking ensemble predictions
- **Feature Engineering**: Custom selection and encoding
- **Preprocessing**: Outlier removal using IQR and normalization techniques

### Performance Metrics

| Model | R² Score | MAE (₹) | RMSE (₹) |
|--------|---------|---------|---------|
| **Random Forest** | 85.92% | 510.86 | 873.03 |
| **XGBoost** | 87.58% | 509.74 | 820.07 |
| **Simple Averaging Ensemble** | 87.64% | 489.17 | 818.11 |
| **Weighted Averaging Ensemble** | 87.77% | 489.75 | 813.79 |
| **Stacking Ensemble (Production Model)** | 87.90% | 489.53 | 809.30 |

### Key Insights
- The **stacking ensemble model** provides the most accurate price predictions.
- Performance validated across multiple commodities and regions.
- Low average error margin of **₹489.53 per 100kg**.
- Robust against market fluctuations with high generalization ability.

## Real-Time Capabilities ⏳

- Dynamic price updates
- Automated retraining pipeline
- Market trend analysis
- Seasonal pattern recognition
- Multi-commodity forecasting

## AI Assistant Capabilities 🤖

- Agricultural best practices
- Crop disease diagnosis
- Weather impact analysis
- Market trends and forecasts
- Government farming schemes
- Multi-lingual support
- Pest control guidance
- Sustainable farming recommendations

## API Endpoints ⚡

- `/` → Main application UI
- `/predict` → Price prediction API
- `/chat` → AI assistant API
- `/get_districts/<state>` → Fetch districts dynamically
- `/get_markets/<district>` → Fetch markets dynamically
- `/get_varieties/<commodity>` → Fetch varieties dynamically

## Large Files Download 📂

Due to GitHub’s file size limits, the following files must be downloaded separately:

1. **Trained Model**
   - File: `stacking_ensemble_model.pkl`
   - Size: ~200MB
   - Place in `models/` directory

2. **Dataset**
   - File: `Price_Agriculture_commodities_Week.csv`
   - Size: ~150MB
   - Place in `data/` directory

## Contribution Guidelines 🤝

We welcome contributions to improve AgroPrice Forecast!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add feature: your-feature-name'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request.

## Contact Information 📧

For queries, suggestions, or collaborations:

**Abdullah Master**   
📧 Email: [abdullahmater2434@gmail.com](mailto:abdullahmater2434@gmail.com)  


## License 📜

This project is licensed under the **SIT License**. See the `LICENSE` file for details.

---
<p align="center">Made with ❤️ by Abdullah Master</p>
<p align="center">© 2024 AgroPrice Forecast. All rights reserved.</p>


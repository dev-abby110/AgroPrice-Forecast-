from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
import json
from groq import Groq

app = Flask(__name__, static_folder='static')
groq_client = Groq(api_key="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")

# Agricultural context and prompt template
AGRICULTURAL_CONTEXT = """You are a multilingual agricultural expert assistant. Follow these rules:
1. Detect the language of the query and respond in the same language (English, Hindi, or Marathi)
2. Keep responses brief and practical (2-3 sentences maximum)
3. Focus on actionable advice for farmers
4. Use simple language that farmers can understand
5. For Hindi and Marathi, use common agricultural terms

Areas of expertise:
- Crop management and disease prevention
- Weather impacts on farming
- Market prices and economics
- Sustainable farming practices
- Soil health and fertilization
- Pest control
- Modern farming technologies
- Government schemes"""

# Load the trained models and other necessary objects
with open('models/stacking_ensemble_model.pkl', 'rb') as f:
    ensemble = pickle.load(f)

rf_model = ensemble['rf_model']
xgb_model = ensemble['xgb_model']
meta_model = ensemble['meta_model']
scaler = ensemble['scaler']
label_encoders = ensemble['label_encoders']
feature_columns = ensemble['feature_columns']

# Load and prepare dropdown data with outlier filtering
df = pd.read_csv('data/Price_Agriculture_commodities_Week.csv')

# Filter out commodities that don't have enough data
commodity_counts = df['Commodity'].value_counts()
valid_commodities = commodity_counts[commodity_counts >= 50].index
df = df[df['Commodity'].isin(valid_commodities)]

# Remove outliers using IQR method
Q1 = df['Modal Price'].quantile(0.25)
Q3 = df['Modal Price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['Modal Price'] >= lower_bound) & (df['Modal Price'] <= upper_bound)]

# Update dropdown data after outlier removal
dropdown_data = {
    'states': sorted(df['State'].unique().tolist()),
    'districts': sorted(df['District'].unique().tolist()),
    'markets': sorted(df['Market'].unique().tolist()),
    'commodities': sorted(valid_commodities.tolist()),
    'varieties': sorted(df['Variety'].unique().tolist()),
    'grades': sorted(df['Grade'].unique().tolist())
}

# Add new route to get district options based on state
@app.route('/get_districts/<state>')
def get_districts(state):
    districts = sorted(df[df['State'] == state]['District'].unique().tolist())
    return jsonify(districts)

# Add new route to get market options based on district
@app.route('/get_markets/<district>')
def get_markets(district):
    markets = sorted(df[df['District'] == district]['Market'].unique().tolist())
    return jsonify(markets)

# Add new route to get variety options based on commodity
@app.route('/get_varieties/<commodity>')
def get_varieties(commodity):
    varieties = sorted(df[df['Commodity'] == commodity]['Variety'].unique().tolist())
    return jsonify(varieties)

@app.route('/')
def index():
    # Load and prepare dropdown data
    df = pd.read_csv('data/Price_Agriculture_commodities_Week.csv')
    dropdown_data = {
        'states': sorted(df['State'].unique().tolist()),
        'districts': sorted(df['District'].unique().tolist()),
        'markets': sorted(df['Market'].unique().tolist()),
        'commodities': sorted(valid_commodities.tolist()),
        'varieties': sorted(df['Variety'].unique().tolist()),
        'grades': sorted(df['Grade'].unique().tolist())
    }
    return render_template('index.html', data=dropdown_data)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Print received data for debugging
        print("Received data:", request.form)
        
        data = request.form.to_dict()
        input_data = []

        # Validate commodity is in valid list
        if data['Commodity'] not in valid_commodities:
            return jsonify({'error': f"Cannot predict prices for {data['Commodity']}. Insufficient historical data."}), 400

        print("Processing features:", feature_columns)
        for col in feature_columns:
            try:
                if col in label_encoders:
                    val = label_encoders[col].transform([data[col]])[0]
                else:
                    val = float(data[col])
                input_data.append(val)
                print(f"Processed {col}: {val}")
            except ValueError as e:
                return jsonify({'error': f"Invalid value for {col}: {data[col]}"}), 400

        input_data = np.array(input_data).reshape(1, -1)
        print("Scaled input shape:", input_data.shape)
        
        input_data_scaled = scaler.transform(input_data)
        
        y_pred_rf = rf_model.predict(input_data_scaled)
        print("RF prediction:", y_pred_rf)
        
        y_pred_xgb = xgb_model.predict(input_data_scaled)
        print("XGB prediction:", y_pred_xgb)
        
        stacked_X = np.column_stack((y_pred_rf, y_pred_xgb))
        y_pred_stack = meta_model.predict(stacked_X)
        print("Final prediction:", y_pred_stack[0])

        return jsonify({'prediction': float(y_pred_stack[0])})
    
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not groq_client.api_key:
            return jsonify({"response": "API key is not configured properly."}), 500
            
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"response": "Please enter a question."}), 400

        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": AGRICULTURAL_CONTEXT
                    },
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ],
                model="llama-3.3-70b-versatile",  # Updated model name
                temperature=0.7,
                max_tokens=800,
                top_p=0.9,
                stream=False
            )
            
            if not chat_completion.choices:
                return jsonify({"response": "No response generated. Please try again."}), 500
                
            response = chat_completion.choices[0].message.content.strip()
            if not response:
                return jsonify({"response": "Empty response received. Please try again."}), 500
                
            return jsonify({"response": response})
            
        except Exception as api_error:
            print(f"API Error: {str(api_error)}")
            return jsonify({"response": "Error: Unable to get response from AI service. Please try again later."}), 503
            
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"response": "An unexpected error occurred. Please try again."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

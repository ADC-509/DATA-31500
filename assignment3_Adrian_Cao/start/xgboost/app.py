from flask import Flask, request, jsonify
from flask_cors import CORS
import xgboost as xgb
import joblib
import numpy as np
import os

# Load the trained model and scaler
model_path = os.getenv('MODEL_PATH', 'xgboost/xgboost_model.json')
scaler_path = os.getenv('SCALER_PATH', 'xgboost/scaler.pkl')
model = xgb.XGBRegressor()
model.load_model(model_path)
scaler = joblib.load(scaler_path)

app = Flask(__name__)
CORS(app)  # For local development; customize for production as needed

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = np.array([
        data['DIABDX_M18'],
        data['ADHDADDX'],
        data['ASTHDX'],
        data['FAMINC22'],
        data['OBTOTV22'],
        data['AGE22X']
    ]).reshape(1, -1)
    
    # Scale the input data
    input_scaled = scaler.transform(input_data)
    
    # Make a prediction
    prediction = model.predict(input_scaled)
    return jsonify({'TOTEXP22_prediction': float(prediction[0])})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

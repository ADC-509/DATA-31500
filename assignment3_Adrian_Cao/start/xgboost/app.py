from flask import Flask, request, jsonify
from flask_cors import CORS
import xgboost as xgb
import numpy as np
import joblib
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths using environment variables or default values
model_path = os.getenv('MODEL_PATH', os.path.join(script_dir, 'xgboost_model.json'))
scaler_path = os.getenv('SCALER_PATH', os.path.join(script_dir, 'scaler.pkl'))

# Load the trained model and scaler
model = xgb.XGBRegressor()
model.load_model(model_path)
scaler = joblib.load(scaler_path)

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})  # Allow all origins; customize in production as needed

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Check if all required fields are in the JSON data
    required_fields = ['DIABDX_M18', 'ADHDADDX', 'ASTHDX', 'FAMINC22', 'OBTOTV22', 'AGE22X']
    if not all(field in data for field in required_fields):
        missing_fields = [field for field in required_fields if field not in data]
        logger.warning(f"Missing fields in request: {missing_fields}")
        return jsonify({'error': f'Missing fields in request: {missing_fields}'}), 400
    
    try:
        # Prepare input data for prediction
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
        logger.info("Prediction successful")
        return jsonify({'TOTEXP22_prediction': float(prediction[0])})
    
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

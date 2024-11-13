from flask import Flask, request, jsonify
from flask_cors import CORS
import xgboost as xgb
import joblib
import numpy as np

# Load the trained model and scaler
model = xgb.XGBRegressor()
model.load_model('C:/Users/a_i_b/OneDrive/文档/GitHub/DATA-31500/assignment3_Adrian_Cao/start/xgboost/xgboost_model.json')
scaler = joblib.load('C:/Users/a_i_b/OneDrive/文档/GitHub/DATA-31500/assignment3_Adrian_Cao/start/xgboost/scaler.pkl')

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from different origins

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
    app.run(debug=True)

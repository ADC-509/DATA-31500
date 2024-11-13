import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths using environment variables or default values
data_path = os.getenv('DATA_PATH', os.path.join(script_dir, 'health_data.csv'))
model_path = os.getenv('MODEL_PATH', os.path.join(script_dir, 'xgboost_model.json'))
scaler_path = os.getenv('SCALER_PATH', os.path.join(script_dir, 'scaler.pkl'))

try:
    # Load the data
    data = pd.read_csv(data_path)
    print("Data loaded successfully.")

    # Prepare the features and target
    X = data[['DIABDX_M18', 'ADHDADDX', 'ASTHDX', 'FAMINC22', 'OBTOTV22', 'AGE22X']]
    y = data['TOTEXP22']

    # Preprocess the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    print("Data preprocessed and split into train/test sets.")

    # Initialize and train the XGBoost model
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=5, learning_rate=0.1)
    model.fit(X_train, y_train)
    print("Model training complete.")

    # Save the model and scaler for later use
    model.save_model(model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model saved to {model_path} and scaler saved to {scaler_path}.")

except FileNotFoundError as e:
    print(f"Error: {e}. Ensure the file path is correct.")
except Exception as e:
    print(f"An error occurred: {e}")

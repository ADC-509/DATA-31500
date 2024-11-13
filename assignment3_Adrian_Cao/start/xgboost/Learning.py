import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib

# Load the data
data = pd.read_csv('start/public/health_data.csv')
X = data[['DIABDX_M18', 'ADHDADDX', 'ASTHDX', 'FAMINC22', 'OBTOTV22', 'AGE22X']]
y = data['TOTEXP22']

# Preprocess the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize and train the XGBoost model
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=5, learning_rate=0.1)
model.fit(X_train, y_train)

# Save the model and scaler for later use
model.save_model('xgboost_model.json')
joblib.dump(scaler, 'scaler.pkl')

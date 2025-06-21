"""
Toronto 311 Dashboard API - Dynamic Charts & ML Predictions
==========================================================
Flask API serving dynamic chart data and ML predictions
(KPI cards remain hardcoded in frontend)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import traceback

app = Flask(__name__)
CORS(app)

# Global variables for cached data
dashboard_data = None
model_data = None

def load_data():
    """Load dashboard data and ML model"""
    global dashboard_data, model_data
    
    try:
        # Load dashboard data (charts)
        insights_path = Path("data/processed/insights.json")
        if insights_path.exists():
            with open(insights_path, 'r') as f:
                dashboard_data = json.load(f)
            print("✅ Dashboard chart data loaded")
        else:
            print("⚠️ insights.json not found - run data pipeline first")
            dashboard_data = None
        
        # Load ML model
        model_path = Path("data/processed/model.joblib")
        if model_path.exists():
            model_data = joblib.load(model_path)
            print("✅ ML model loaded")
        else:
            print("⚠️ model.joblib not found - run data pipeline first")
            model_data = None
            
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        dashboard_data = None
        model_data = None

@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """Get dynamic chart data for dashboard"""
    
    if dashboard_data is None:
        return jsonify({
            "status": "error",
            "message": "Dashboard data not available. Run data_pipeline.py first."
        }), 500
    
    return jsonify({
        "status": "success",
        "data": dashboard_data,
        "last_updated": dashboard_data.get("generated_at", datetime.now().isoformat())
    })

@app.route('/api/predict-completion', methods=['POST'])
def predict_completion():
    """Predict service request completion likelihood"""
    
    if model_data is None:
        return jsonify({
            "status": "error",
            "message": "ML model not available. Run data_pipeline.py first."
        }), 500
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        # Validate required fields
        required_fields = ['service_type', 'ward', 'division']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Prepare features for prediction
        prediction_result = make_prediction(data)
        
        return jsonify({
            "status": "success",
            "prediction": prediction_result
        })
        
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": f"Prediction failed: {str(e)}"
        }), 500

def make_prediction(input_data):
    """Make ML prediction based on input data"""
    
    # Extract model components
    model = model_data['model']
    feature_columns = model_data['feature_columns']
    categorical_values = model_data['categorical_values']
    
    # Prepare feature vector
    features = pd.DataFrame(0, index=[0], columns=feature_columns)
    
    # Map categorical features (one-hot encoding)
    service_type = input_data.get('service_type', '')
    ward = input_data.get('ward', '')
    division = input_data.get('division', '')
    
    # Set one-hot encoded features
    for col in feature_columns:
        if col.startswith('Service Request Type_') and service_type in col:
            features.loc[0, col] = 1
        elif col.startswith('Ward_') and ward in col:
            features.loc[0, col] = 1
        elif col.startswith('Division_') and division in col:
            features.loc[0, col] = 1
    
    # Map temporal features
    time_mapping = {
        'morning': 9, 'afternoon': 14, 'evening': 19, 'night': 2
    }
    day_mapping = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    # Set temporal features
    if 'Month' in feature_columns:
        features.loc[0, 'Month'] = datetime.now().month
    
    if 'Weekday' in feature_columns:
        day_of_week = input_data.get('day_of_week', '').lower()
        features.loc[0, 'Weekday'] = day_mapping.get(day_of_week, 1)
    
    if 'Hour' in feature_columns:
        time_of_day = input_data.get('time_of_day', '').lower()
        features.loc[0, 'Hour'] = time_mapping.get(time_of_day, 12)
    
    # Make prediction
    prediction_proba = model.predict_proba(features)[0]
    prediction = model.predict(features)[0]
    
    # Format results
    completion_probability = prediction_proba[1] * 100  # Probability of completion (class 1)
    confidence = max(prediction_proba) * 100
    
    # Determine prediction text
    if completion_probability >= 70:
        prediction_text = "Highly Likely to be Completed"
    elif completion_probability >= 50:
        prediction_text = "Likely to be Completed"
    elif completion_probability >= 30:
        prediction_text = "May be Completed"
    else:
        prediction_text = "Unlikely to be Completed"
    
    # Generate influencing factors
    factors = generate_factors(input_data, completion_probability)
    
    return {
        "prediction": prediction_text,
        "completion_probability": f"{completion_probability:.1f}",
        "confidence": f"{confidence:.1f}",
        "factors": factors
    }

def generate_factors(input_data, probability):
    """Generate factors that influence the prediction"""
    factors = []
    
    # Add input-based factors
    if input_data.get('service_type'):
        factors.append(f"Service Type: {input_data['service_type']}")
    
    if input_data.get('ward'):
        factors.append(f"Ward: {input_data['ward']}")
    
    if input_data.get('division'):
        factors.append(f"Division: {input_data['division']}")
    
    if input_data.get('time_of_day'):
        factors.append(f"Time of Day: {input_data['time_of_day'].title()}")
    
    if input_data.get('day_of_week'):
        factors.append(f"Day of Week: {input_data['day_of_week'].title()}")
    
    # Add probability-based insights
    if probability > 80:
        factors.append("Historical data shows high completion rate for similar requests")
    elif probability > 60:
        factors.append("Moderate completion likelihood based on patterns")
    elif probability < 40:
        factors.append("Lower completion rate - may need follow-up")
    
    return factors[:5]  # Return top 5 factors

@app.route('/api/categorical-values', methods=['GET'])
def get_categorical_values():
    """Get available categorical values for dropdowns"""
    
    if dashboard_data is None:
        return jsonify({
            "status": "error",
            "message": "Data not available"
        }), 500
    
    categorical_values = dashboard_data.get('categorical_values', {})
    
    return jsonify({
        "status": "success",
        "data": categorical_values
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "chart_data_available": dashboard_data is not None,
        "ml_model_available": model_data is not None,
        "message": "Backend ready for dynamic charts and ML predictions"
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Toronto 311 Dashboard API - Dynamic Charts & ML Predictions",
        "version": "1.0.0",
        "endpoints": {
            "charts": "/api/dashboard-data",
            "prediction": "/api/predict-completion (POST)",
            "dropdowns": "/api/categorical-values",
            "health": "/api/health"
        },
        "note": "KPI cards are hardcoded in frontend - this API serves dynamic charts and ML predictions"
    })

if __name__ == '__main__':
    print("🚀 Starting Toronto 311 Dashboard API...")
    print("📊 Focus: Dynamic charts and ML predictions")
    print("💡 Note: KPI cards remain hardcoded in frontend")
    
    # Load data on startup
    load_data()
    
    print(f"\n📈 Chart data available: {dashboard_data is not None}")
    print(f"🤖 ML model available: {model_data is not None}")
    
    if dashboard_data is None or model_data is None:
        print("\n⚠️  Run 'python data_pipeline/data_pipeline.py' first!")
    
    print("\n🌐 API running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

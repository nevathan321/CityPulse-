"""
Toronto 311 Data Pipeline - Dynamic Charts & ML Model
====================================================
Processes CSV data to generate:
1. Dynamic chart data for frontend
2. Trained ML model for completion predictions
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
from pathlib import Path

class Toronto311Pipeline:
    def __init__(self, csv_path="data/raw/SR2025.csv"):
        self.csv_path = csv_path
        self.df = None
        self.model = None
        self.label_encoder = None
        self.feature_columns = None
        self.categorical_encoders = {}
        
    def load_and_clean_data(self):
        """Load and clean the CSV data"""
        print("📊 Loading CSV data...")
        
        # Load CSV with error handling
        self.df = pd.read_csv(self.csv_path, encoding="latin1", on_bad_lines="skip")
        self.df.columns = self.df.columns.str.strip()
        
        print(f"✅ Loaded {len(self.df)} records")
        print(f"📋 Columns: {list(self.df.columns)}")
        
        # Clean and prepare data
        print("🧹 Cleaning data...")
        
        # Drop rows missing essential values
        essential_cols = ['Status', 'Service Request Type', 'Division', 'Ward', 'Creation Date']
        initial_count = len(self.df)
        self.df = self.df.dropna(subset=essential_cols)
        print(f"Removed {initial_count - len(self.df)} rows with missing essential data")
        
        # Parse dates
        self.df['Creation Date'] = pd.to_datetime(self.df['Creation Date'], errors='coerce')
        self.df = self.df.dropna(subset=['Creation Date'])
        
        # Extract temporal features
        self.df['Date'] = self.df['Creation Date'].dt.date
        self.df['Month'] = self.df['Creation Date'].dt.month
        self.df['Weekday'] = self.df['Creation Date'].dt.dayofweek
        self.df['Hour'] = self.df['Creation Date'].dt.hour
        self.df['DayOfWeek'] = self.df['Creation Date'].dt.day_name()
        
        # Clean status values
        self.df['Status'] = self.df['Status'].str.strip()
        
        print(f"✅ Cleaned data: {len(self.df)} records remaining")
        
    def generate_chart_data(self):
        """Generate data specifically for dynamic charts"""
        print("📈 Generating chart data...")
        
        chart_data = {}
        
        # 1. Time Series Chart - Daily requests over time
        daily_counts = self.df.groupby('Date').size().reset_index(name='count')
        daily_counts['Date'] = daily_counts['Date'].astype(str)
        # Get last 30 days for better visualization
        chart_data["time_series"] = {
            "dates": daily_counts['Date'].tolist()[-30:],
            "counts": [int(x) for x in daily_counts['count'].tolist()[-30:]]
        }
        
        # 2. Ward Distribution Chart - Top 15 wards
        ward_counts = self.df['Ward'].value_counts().head(15)
        chart_data["ward_distribution"] = {
            "wards": ward_counts.index.tolist(),
            "counts": [int(x) for x in ward_counts.values.tolist()]
        }
        
        # 3. Status Distribution Chart - Pie chart data
        status_counts = self.df['Status'].value_counts()
        chart_data["status_distribution"] = {
            "statuses": status_counts.index.tolist(),
            "counts": [int(x) for x in status_counts.values.tolist()]
        }
        
        # 4. Service Types Chart - Top 15 service types
        service_counts = self.df['Service Request Type'].value_counts().head(15)
        chart_data["service_types"] = {
            "types": service_counts.index.tolist(),
            "counts": [int(x) for x in service_counts.values.tolist()]
        }
        
        # 5. Division Distribution Chart - Top 10 divisions
        division_counts = self.df['Division'].value_counts().head(10)
        chart_data["division_distribution"] = {
            "divisions": division_counts.index.tolist(),
            "counts": [int(x) for x in division_counts.values.tolist()]
        }
        
        # 6. Hourly Pattern Chart - Requests by hour of day
        hourly_counts = self.df.groupby('Hour').size()
        chart_data["hourly_pattern"] = {
            "hours": list(range(24)),
            "counts": [int(hourly_counts.get(h, 0)) for h in range(24)]
        }
        
        return chart_data
    
    def train_ml_model(self):
        """Train ML model for completion prediction"""
        print("🤖 Training ML model for completion prediction...")
        
        # Create binary target: completed vs not completed
        completed_statuses = ['Closed', 'Completed']
        self.df['Completed'] = self.df['Status'].isin(completed_statuses).astype(int)
        
        print(f"Completion rate: {self.df['Completed'].mean():.2%}")
        
        # Prepare features for ML model
        categorical_features = ['Service Request Type', 'Division', 'Ward']
        
        # Create feature matrix
        feature_data = []
        
        # One-hot encode categorical features
        for col in categorical_features:
            encoded = pd.get_dummies(self.df[col], prefix=col, drop_first=True)
            feature_data.append(encoded)
        
        # Add temporal features
        temporal_features = self.df[['Month', 'Weekday', 'Hour']]
        feature_data.append(temporal_features)
        
        # Combine all features
        X = pd.concat(feature_data, axis=1)
        y = self.df['Completed']
        
        # Store feature columns for prediction
        self.feature_columns = X.columns.tolist()
        
        # Store unique values for each categorical feature (for prediction validation)
        self.categorical_values = {
            'service_types': sorted(self.df['Service Request Type'].unique().tolist()),
            'divisions': sorted(self.df['Division'].unique().tolist()),
            'wards': sorted(self.df['Ward'].unique().tolist())
        }
        
        print(f"Feature matrix shape: {X.shape}")
        print(f"Features: {len(self.feature_columns)} total")
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        # Train Random Forest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"✅ Model Performance:")
        print(f"   Accuracy:  {accuracy:.3f}")
        print(f"   Precision: {precision:.3f}")
        print(f"   Recall:    {recall:.3f}")
        print(f"   F1-Score:  {f1:.3f}")
        
        # Feature importance for insights
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False).head(10)
        
        return {
            "features": feature_importance['feature'].tolist(),
            "importance": [round(imp, 4) for imp in feature_importance['importance'].tolist()]
        }
    
    def save_outputs(self):
        """Save chart data and ML model"""
        print("💾 Saving outputs...")
        
        # Create processed directory
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate chart data
        chart_data = self.generate_chart_data()
        
        # Train model and get feature importance
        feature_importance = self.train_ml_model()
        
        # Combine all data for frontend
        dashboard_data = {
            "generated_at": datetime.now().isoformat(),
            "total_records": int(len(self.df)),  # Convert to int
            "date_range": {
                "start": self.df['Creation Date'].min().isoformat(),
                "end": self.df['Creation Date'].max().isoformat()
            },
            **chart_data,
            "feature_importance": feature_importance,
            "categorical_values": self.categorical_values
        }
        
        # Save dashboard data
        insights_path = processed_dir / "insights.json"
        with open(insights_path, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        print(f"✅ Saved chart data to {insights_path}")
        
        # Save ML model and metadata
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns,
            'categorical_values': self.categorical_values
        }
        
        model_path = processed_dir / "model.joblib"
        joblib.dump(model_data, model_path)
        print(f"✅ Saved ML model to {model_path}")
        
    def run_pipeline(self):
        """Run the complete pipeline"""
        print("🚀 Starting Toronto 311 Data Pipeline...")
        
        try:
            self.load_and_clean_data()
            self.save_outputs()
            print("\n✅ Pipeline completed successfully!")
            print("🎯 Generated:")
            print("   📊 Dynamic chart data for frontend")
            print("   🤖 ML model for completion predictions")
            print("\n🚀 Ready to start Flask backend!")
            
        except Exception as e:
            print(f"❌ Pipeline failed: {str(e)}")
            raise

def main():
    """Main execution function"""
    pipeline = Toronto311Pipeline()
    pipeline.run_pipeline()

if __name__ == "__main__":
    main()

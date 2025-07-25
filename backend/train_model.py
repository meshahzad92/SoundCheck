#!/usr/bin/env python3
"""
NHANES Hearing Loss Classification Model Training
Based on the SoundCheck application requirements from the hackathon PDF.
"""

import pandas as pd
import numpy as np
import pyreadstat
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import os

def load_nhanes_data(file_path):
    """Load NHANES audiometry data from XPT file"""
    print("Loading NHANES audiometry data...")
    df, meta = pyreadstat.read_xport(file_path)
    print(f"Loaded {len(df)} records with {len(df.columns)} columns")
    print("=======================================")
    print(df.head())
    return df, meta

def clean_and_prepare_data(df):
    """Clean and prepare the audiometry data for ML training"""
    print("Cleaning and preparing data...")
    
    # Define frequency mapping for hearing thresholds
    freq_map = {
        '500': ['AUXU500R', 'AUXU500L'],
        '1000': ['AUXU1K1R', 'AUXU1K1L'], 
        '2000': ['AUXU2KR', 'AUXU2KL'],
        '3000': ['AUXU3KR', 'AUXU3KL'],
        '4000': ['AUXU4KR', 'AUXU4KL'],
        '6000': ['AUXU6KR', 'AUXU6KL'],
        '8000': ['AUXU8KR', 'AUXU8KL']
    }
    
    # Replace invalid values (666, 777, 888) with NaN
    print("Replacing invalid values...")
    for cols in freq_map.values():
        for col in cols:
            if col in df.columns:
                df[col] = df[col].replace({666: np.nan, 777: np.nan, 888: np.nan})
    
    # Compute average threshold across ears for each frequency
    print("Computing average thresholds across ears...")
    for freq, (r_col, l_col) in freq_map.items():
        if r_col in df.columns and l_col in df.columns:
            df[f'{freq}_avg'] = df[[r_col, l_col]].mean(axis=1)
        elif r_col in df.columns:
            df[f'{freq}_avg'] = df[r_col]
        elif l_col in df.columns:
            df[f'{freq}_avg'] = df[l_col]
    
    # Create Pure-Tone Average (PTA) for 500, 1000, 2000, 4000 Hz
    print("Computing Pure-Tone Average (PTA)...")
    pta_freqs = ['500_avg', '1000_avg', '2000_avg', '4000_avg']
    available_pta_freqs = [freq for freq in pta_freqs if freq in df.columns]
    
    if available_pta_freqs:
        df['PTA'] = df[available_pta_freqs].mean(axis=1)
    else:
        print("Warning: No PTA frequencies available, using available frequencies")
        available_freqs = [f'{freq}_avg' for freq in freq_map.keys() if f'{freq}_avg' in df.columns]
        if available_freqs:
            df['PTA'] = df[available_freqs].mean(axis=1)
    
    return df, freq_map

def classify_hearing_loss(pta):
    """Classify hearing loss based on PTA (Pure-Tone Average)"""
    if pd.isna(pta):
        return np.nan
    elif pta <= 25:
        return 'Normal'
    elif pta <= 40:
        return 'Mild'
    elif pta <= 60:
        return 'Moderate'
    elif pta <= 80:
        return 'Severe'
    else:
        return 'Profound'

def prepare_features_and_target(df, freq_map):
    """Prepare feature matrix X and target vector y"""
    print("Preparing features and target...")
    
    # Apply hearing loss classification
    df['hearing_category'] = df['PTA'].apply(classify_hearing_loss)
    
    # Create feature matrix using available frequency averages
    feature_cols = [f'{freq}_avg' for freq in freq_map.keys() if f'{freq}_avg' in df.columns]
    
    print(f"Available feature columns: {feature_cols}")
    
    # Drop rows with missing values
    df_clean = df.dropna(subset=feature_cols + ['PTA', 'hearing_category'])
    
    print(f"Clean dataset size: {len(df_clean)} records")
    print(f"Hearing category distribution:")
    print(df_clean['hearing_category'].value_counts())
    
    X = df_clean[feature_cols]
    y = df_clean['hearing_category']
    
    return X, y, df_clean

def train_models(X, y):
    """Train multiple ML models and return the best one"""
    print("Training ML models...")

    # Handle class imbalance - remove classes with too few samples or don't stratify
    class_counts = y.value_counts()
    print(f"Class distribution: {class_counts}")

    # Filter out classes with only 1 sample for stratification
    min_samples_per_class = 2
    valid_classes = class_counts[class_counts >= min_samples_per_class].index

    if len(valid_classes) < len(class_counts):
        print(f"Removing classes with < {min_samples_per_class} samples: {set(class_counts.index) - set(valid_classes)}")
        mask = y.isin(valid_classes)
        X = X[mask]
        y = y[mask]
        print(f"Filtered dataset size: {len(X)} records")

    # Split the data with stratification if possible
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print("Using stratified split")
    except ValueError:
        # Fall back to random split if stratification fails
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        print("Using random split (stratification failed)")
    
    # Scale features for logistic regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'DecisionTree': DecisionTreeClassifier(random_state=42, max_depth=10),
        'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000)
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        if name == 'LogisticRegression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"{name} Accuracy: {accuracy:.4f}")
        print(f"Classification Report for {name}:")
        print(classification_report(y_test, y_pred))
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'predictions': y_pred,
            'scaler': scaler if name == 'LogisticRegression' else None
        }
        
        if accuracy > best_score:
            best_score = accuracy
            best_model = model
            best_name = name
    
    print(f"\nBest model: {best_name} with accuracy: {best_score:.4f}")
    
    return results, best_model, best_name, scaler if best_name == 'LogisticRegression' else None

def save_model_and_artifacts(model, model_name, scaler, feature_names):
    """Save the trained model and related artifacts"""
    print("Saving model and artifacts...")
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save the model
    model_path = f'models/hearing_classifier_{model_name.lower()}.joblib'
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")
    
    # Save scaler if used
    if scaler is not None:
        scaler_path = 'models/scaler.joblib'
        joblib.dump(scaler, scaler_path)
        print(f"Scaler saved to: {scaler_path}")
    
    # Save feature names
    feature_path = 'models/feature_names.joblib'
    joblib.dump(feature_names, feature_path)
    print(f"Feature names saved to: {feature_path}")
    
    # Save model metadata
    metadata = {
        'model_name': model_name,
        'feature_names': feature_names,
        'uses_scaler': scaler is not None,
        'classes': list(model.classes_) if hasattr(model, 'classes_') else None
    }
    
    metadata_path = 'models/model_metadata.joblib'
    joblib.dump(metadata, metadata_path)
    print(f"Model metadata saved to: {metadata_path}")

def main():
    """Main training pipeline"""
    print("Starting NHANES Hearing Loss Model Training...")
    
    # Load data
    df, meta = load_nhanes_data('AUX_J.xpt')
    
    # Clean and prepare data
    df_clean, freq_map = clean_and_prepare_data(df)
    
    # Prepare features and target
    print("=======================================")
    print("Cleaned data: ", df_clean.head())
    print("=======================================")
    X, y, df_final = prepare_features_and_target(df_clean, freq_map)
    print("Final feature matrix X: ", X.head())
    print("Final target vector y: ", y.head())
    if len(X) == 0:
        print("Error: No valid data available for training!")
        return
    
    # Train models
    results, best_model, best_name, scaler = train_models(X, y)
    
    # Save the best model
    save_model_and_artifacts(best_model, best_name, scaler, list(X.columns))
    
    print("\nTraining completed successfully!")
    print(f"Best model: {best_name}")
    print(f"Feature columns: {list(X.columns)}")

if __name__ == "__main__":
    main()

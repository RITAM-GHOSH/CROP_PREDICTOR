import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from crop_data import get_dataset

def train_model():
    """
    Trains a machine learning model for crop recommendation.
    
    Returns:
        tuple: (trained model, label encoder)
    """
    # Get the dataset
    df = get_dataset()
    
    if df is None or df.empty:
        raise ValueError("Failed to load dataset for model training")
    
    # Prepare features and target
    X = df.drop('label', axis=1)
    y = df['label']
    
    # Encode the target labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Train a Random Forest classifier
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    
    # Train on the entire dataset for deployment
    model.fit(X, y_encoded)
    
    return model, label_encoder

def predict_crop(model, label_encoder, input_data):
    """
    Predicts crops based on input environmental conditions.
    
    Args:
        model: Trained machine learning model
        label_encoder: Label encoder used during training
        input_data: Array of environmental conditions
        
    Returns:
        tuple: (predicted crop, probability distribution)
    """
    # Make prediction
    prediction = model.predict(input_data)
    
    # Get probability distribution
    probabilities = model.predict_proba(input_data)
    
    return prediction, probabilities

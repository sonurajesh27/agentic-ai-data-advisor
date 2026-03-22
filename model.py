"""
model.py - ML model training for data usage prediction
Uses Linear Regression trained on synthetic data
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os

def generate_training_data(n_samples=500):
    """Generate synthetic training data for data usage prediction."""
    np.random.seed(42)

    # Features: [daily_hours, streams_video (0/1), num_downloads, social_media_hours]
    daily_hours = np.random.uniform(1, 12, n_samples)
    streams_video = np.random.randint(0, 2, n_samples)
    num_downloads = np.random.randint(0, 20, n_samples)
    social_media_hours = np.random.uniform(0, 6, n_samples)

    # Target: data usage in GB
    # Rough formula: streaming ~2GB/hr, browsing ~0.1GB/hr, downloads ~0.5GB each, social ~0.3GB/hr
    data_usage = (
        daily_hours * 0.1
        + streams_video * daily_hours * 1.8
        + num_downloads * 0.5
        + social_media_hours * 0.3
        + np.random.normal(0, 0.3, n_samples)  # noise
    )
    data_usage = np.clip(data_usage, 0.1, None)

    X = np.column_stack([daily_hours, streams_video, num_downloads, social_media_hours])
    return X, data_usage


def train_model():
    """Train and save the Linear Regression model."""
    X, y = generate_training_data()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print("Model trained and saved.")
    return model, scaler


def load_model():
    """Load saved model and scaler, training if not found."""
    if not os.path.exists("model.pkl") or not os.path.exists("scaler.pkl"):
        return train_model()

    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    return model, scaler


def predict_usage(daily_hours, streams_video, num_downloads, social_media_hours):
    """
    Predict daily data usage in GB.

    Args:
        daily_hours (float): Total daily internet usage in hours
        streams_video (int): 1 if user streams video, 0 otherwise
        num_downloads (int): Number of file downloads per day
        social_media_hours (float): Hours spent on social media

    Returns:
        float: Predicted data usage in GB
    """
    model, scaler = load_model()
    features = np.array([[daily_hours, streams_video, num_downloads, social_media_hours]])
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    return round(max(prediction, 0.1), 2)


if __name__ == "__main__":
    train_model()
    sample = predict_usage(6, 1, 5, 2)
    print(f"Sample prediction: {sample} GB")

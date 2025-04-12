# model_training.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_model():
    # Load data
    train_df = pd.read_csv('data/train.csv')
    test_df = pd.read_csv('data/test.csv')
    
    # Combine train and test data for better training
    df = pd.concat([train_df, test_df], axis=0)
    
    # Separate features and target
    X = df.drop('fake', axis=1)
    y = df['fake']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Initialize and train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    if not os.path.exists('models'):
        os.makedirs('models')
    joblib.dump(model, 'models/random_forest_model.pkl')
    print("Model saved successfully!")

if __name__ == "__main__":
    train_model()

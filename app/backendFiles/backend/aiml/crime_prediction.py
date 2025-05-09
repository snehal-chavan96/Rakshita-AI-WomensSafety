import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("aiml/crime_data.csv")  # Ensure this has 'latitude', 'longitude', and 'crime_level'

# Define input and output
X = data[['Latitude', 'Longitude']]
y = data['Crime_Type']  # This should be a category like "High", "Medium", "Low"

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)


# Define the model save path
model_path = os.path.join("backend", "aiml", "crime_model.pkl")
model = joblib.load(model_path)


# Ensure directory exists
os.makedirs(os.path.dirname(model_path), exist_ok=True)

# Save trained model
joblib.dump(model, model_path)
print("Model trained and saved successfully at:", model_path)


def predict_crime(latitude, longitude):
    # Load the trained model
    model = joblib.load("crime_model.pkl")

    # Make a prediction
    prediction = model.predict([[latitude, longitude]])
    
    return prediction[0]



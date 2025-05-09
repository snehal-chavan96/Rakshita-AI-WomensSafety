from flask import Blueprint, request, jsonify
from aiml.crime_prediction import predict_crime

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json
    crime_type = predict_crime(data['latitude'], data['longitude'])
    return jsonify({"predicted_crime": crime_type}), 200

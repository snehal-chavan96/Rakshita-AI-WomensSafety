from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import db, init_db
from routes.auth import auth_bp
from routes.report import report_bp
from routes.predict import predict_bp
from aiml.crime_prediction import predict_crime

app = Flask(__name__)
CORS(app)

# ✅ Add JWT secret key for authentication
app.config['JWT_SECRET_KEY'] = 'secret_key'  # Replace with a strong key

init_db(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(report_bp, url_prefix='/api/reports')
app.register_blueprint(predict_bp, url_prefix='/api/ml')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, request, jsonify
from models.report import Report, db
from flask_jwt_extended import jwt_required, get_jwt_identity

report_bp = Blueprint('report', __name__)

@report_bp.route('/report', methods=['POST'])
# @jwt_required()
def report_crime():
    data = request.json
    user_id = 1
    report = Report(
        user_id=user_id,
        latitude=data['latitude'],
        longitude=data['longitude'],
        crime_type=data['crime_type'],
        description=data.get('description')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({"message": "Report submitted successfully"}), 201

@report_bp.route('/reports', methods=['GET'])
def get_reports():
    reports = Report.query.all()
    return jsonify([{"id": r.id, "latitude": r.latitude, "longitude": r.longitude, "crime_type": r.crime_type} for r in reports]), 200

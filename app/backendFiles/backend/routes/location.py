from flask import Blueprint, request, jsonify
from database import db
from models.live_location import LiveLocation
from models.route_history import RouteHistory

location_bp = Blueprint('location_bp', __name__)

# Save a new live location
@location_bp.route('/api/location', methods=['POST'])
def save_live_location():
    data = request.get_json()
    try:
        location = LiveLocation(
            user_id=data['user_id'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        db.session.add(location)
        db.session.commit()
        return jsonify({'message': 'Live location saved successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Save a new route history
@location_bp.route('/api/route', methods=['POST'])
def save_route_history():
    data = request.get_json()
    try:
        route = RouteHistory(
            user_id=data['user_id'],
            route_taken=data['route_taken'],  # This should be a list or GeoJSON
            started_at=data.get('started_at'),
            ended_at=data.get('ended_at'),
            status=data.get('status', 'Safe')
        )
        db.session.add(route)
        db.session.commit()
        return jsonify({'message': 'Route history saved successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Get all routes of a user
@location_bp.route('/api/route/<int:user_id>', methods=['GET'])
def get_user_routes(user_id):
    try:
        routes = RouteHistory.query.filter_by(user_id=user_id).all()
        route_list = [
            {
                "id": r.id,
                "route_taken": r.route_taken,
                "started_at": r.started_at,
                "ended_at": r.ended_at,
                "status": r.status
            } for r in routes
        ]
        return jsonify(route_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

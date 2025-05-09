from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS
import requests
ORS_API_KEY = '5b3ce3597851110001cf624803ef98d8bc9b4635bb02d9f8e13f46a0'  # replace with your actual key


app = Flask(__name__)
CORS(app)  # Allow requests from Android app

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="rakshita_db",
        user="postgres",
        password="pournima"
    )

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({'status': 'fail', 'error': 'Missing fields'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO signup (username, email, password)
            VALUES (%s, %s, %s)
        """, (username, email, password))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'status': 'fail', 'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT * FROM signup WHERE username = %s AND password = %s
        """, (username, password))
        user = cur.fetchone()
        if user:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'fail', 'error': 'Invalid credentials'}), 401
    except psycopg2.Error as e:
        return jsonify({'status': 'fail', 'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/update_details', methods=['POST'])
def update_details():
    data = request.get_json()
    username = data.get('username')
    contact = data.get('contact')
    address = data.get('address')
    trusted_contacts = data.get('trusted_contacts')

    if not username:
        return jsonify({'status': 'fail', 'error': 'Username is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE signup 
            SET contact = %s, address = %s, trusted_contacts = %s
            WHERE username = %s
        """, (contact, address, trusted_contacts, username))
        conn.commit()
        return jsonify({'status': 'success'}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'status': 'fail', 'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/get_trusted_contact', methods=['POST'])
def get_trusted_contact():
    data = request.get_json()
    username = data.get('username')

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT trusted_contacts FROM signup WHERE username = %s", (username,))
        result = cur.fetchone()
        if result and result[0]:
            trusted_contact = result[0].strip("{}")  # Remove braces if stored in array form
            return jsonify({'status': 'success', 'trusted_contact': trusted_contact}), 200
        else:
            return jsonify({'status': 'fail', 'error': 'No trusted contact found'}), 404
    except Exception as e:
        return jsonify({'status': 'fail', 'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()



ORS_API_KEY = "5b3ce3597851110001cf624803ef98d8bc9b4635bb02d9f8e13f46a0"

# Convert Address to Coordinates using OpenRouteService Geocoding API
def get_coordinates(address):
    url = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_API_KEY}&text={address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        results = response.json()
        if results["features"]:
            coordinates = results["features"][0]["geometry"]["coordinates"]
            return [coordinates[0], coordinates[1]]  # [lng, lat]
    
    return None  # Address not found

@app.route('/safer-route', methods=['POST'])
def get_safer_route():
    data = request.json
    origin_address = data['origin']
    destination_address = data['destination']

    # Convert city names to latitude & longitude
    origin = get_coordinates(origin_address)
    destination = get_coordinates(destination_address)

    if not origin or not destination:
        return jsonify({"error": "Invalid origin or destination"}), 400

    # Step 1: Get Routes from OpenRouteService
    ors_url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
    "coordinates": [origin, destination],
    "instructions": False,
    "radiuses": [-1, -1],
    "alternative_routes": {
        "share_factor": 0.6,
        "target_count": 3,
        "weight_factor": 1.6
    }
}


    response = requests.post(ors_url, json=payload, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": f"Failed to fetch routes: {response.json()}"}), 500

    routes = response.json()["features"]

    # Step 2: Hardcoded Unsafe Locations (lat, lng, severity)
    unsafe_zones = [
        (18.5204, 73.8567, 5), (18.6432, 73.8993, 4), (18.5649, 73.7769, 3),
        (18.5912, 73.7387, 2), (18.5236, 73.8478, 4), (18.5006, 73.8215, 3),
        (18.6083, 73.8309, 4), (18.6180, 73.8679, 3), (18.5309, 73.8502, 2),
        (18.4745, 73.8626, 1), (18.5698, 73.7895, 3), (18.5074, 73.8077, 5),
        (18.6543, 73.8292, 2), (18.6511, 73.8580, 3), (18.5832, 73.8095, 1),
        (18.4647, 73.7521, 5), (18.6594, 73.8984, 3), (18.6825, 73.7849, 1),
        (18.5644, 73.8974, 3), (18.6371, 73.8883, 2), (18.5984, 73.8641, 2),
        (18.5796, 73.8829, 3), (18.6931, 73.8781, 4), (18.6764, 73.8236, 3),
        (18.5114, 73.7998, 4), (18.5534, 73.7421, 4), (18.5441, 73.8087, 1),
        (18.6897, 73.7401, 1), (18.6714, 73.7746, 2), (18.5162, 73.7413, 1),
        (18.6769, 73.8701, 2), (18.5814, 73.8504, 3), (18.5564, 73.7482, 5),
        (18.4734, 73.8651, 2), (18.6509, 73.7404, 1), (18.6487, 73.8093, 2),
        (18.4586, 73.7801, 3), (18.6195, 73.7429, 5), (18.6328, 73.7864, 3),
        (18.5301, 73.8957, 2), (18.6805, 73.7968, 4), (18.4589, 73.8294, 3),
        (18.4943, 73.8087, 5), (18.6221, 73.8993, 1), (18.6407, 73.8879, 4),
        (18.4554, 73.7407, 2), (18.5744, 73.8765, 3), (18.4897, 73.8774, 3),
        (18.5124, 73.7542, 1), (18.6517, 73.8456, 4), (18.5248, 73.7412, 2),
        (18.6725, 73.8237, 5), (18.6872, 73.8532, 3), (18.6094, 73.7498, 3),
        (18.5334, 73.7639, 1), (18.4846, 73.8751, 4), (18.4869, 73.7574, 1),
        (18.4664, 73.7991, 5), (18.5446, 73.8952, 4), (18.5963, 73.7423, 2),
        (18.4718, 73.7654, 2), (18.6618, 73.8861, 1), (18.6004, 73.8504, 4),
        (18.5923, 73.7935, 3), (18.4563, 73.8764, 2), (18.4981, 73.8432, 3),
        (18.6476, 73.8523, 2), (18.5523, 73.8123, 5), (18.4826, 73.8443, 1),
        (18.6754, 73.7705, 1), (18.5522, 73.8589, 4), (18.6331, 73.7507, 2),
        (18.6485, 73.7485, 5), (18.5476, 73.8692, 3), (18.5387, 73.8311, 1),
        (18.6759, 73.8881, 4), (18.4577, 73.8412, 2), (18.6234, 73.8541, 2),
        (18.6592, 73.7814, 3), (18.6438, 73.7526, 1), (18.4621, 73.8563, 4),
        (18.5741, 73.7602, 3), (18.5031, 73.7811, 1), (18.6651, 73.8719, 5),
        (18.4669, 73.8811, 4), (18.6753, 73.8965, 3), (18.5528, 73.7404, 2),
        (18.4593, 73.7525, 4), (18.6107, 73.8787, 2), (18.5838, 73.7956, 5),
        (18.5899, 73.8931, 4), (18.6677, 73.7385, 3), (18.6015, 73.7856, 1),
        (18.5934, 73.8263, 2), (18.6777, 73.7924, 3), (18.6653, 73.8347, 4),
        (18.4715, 73.7401, 3), (18.6436, 73.8377, 1), (18.4862, 73.7399, 2),
        (18.6688, 73.7661, 5), (18.6609, 73.8701, 1), (18.4724, 73.8147, 2),
        (18.5854, 73.8734, 3), (18.6552, 73.8824, 5), (18.5247, 73.7937, 1)
    ]


    # Step 3: Assign Safety Colors to Routes
    def get_colored_segments(route):
        coords = route["geometry"]["coordinates"]
        colored_segments = []

        for i in range(len(coords) - 1):
            start = coords[i]
            end = coords[i + 1]

            lat1, lng1 = start[1], start[0]
            lat2, lng2 = end[1], end[0]

            # Default severity
            max_severity = 0

            for zone in unsafe_zones:
                unsafe_lat, unsafe_lng, severity = zone
                # Check if either point is close to a danger zone
                if (abs(lat1 - unsafe_lat) < 0.01 and abs(lng1 - unsafe_lng) < 0.01) or \
                (abs(lat2 - unsafe_lat) < 0.01 and abs(lng2 - unsafe_lng) < 0.01):
                    max_severity = max(max_severity, severity)

            # Color based on severity
            if max_severity == 0:
                color = "green"
            elif max_severity == 1:
                color = "yellow"
            elif max_severity == 2:
                color = "orange"
            else:
                color = "red"

            colored_segments.append({
                "segment": [start, end],
                "color": color
            })

        return colored_segments

    # Step 4: Attach Colors to Routes
    segments_with_colors = []
    for route in routes:
        segments = get_colored_segments(route)
        segments_with_colors.extend(segments)

    return jsonify({"segments": segments_with_colors})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Use 0.0.0.0 for Android access

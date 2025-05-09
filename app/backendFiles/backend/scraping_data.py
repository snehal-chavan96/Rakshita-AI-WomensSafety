import sqlalchemy
from datetime import datetime
import re

# PostgreSQL DB connection
DB_USER = 'postgres'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'rakshita_db'

engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Sample scraped data (you can automate this later)
paragraphs = [
    "It may be recalled that a 21-year-old woman and her 22-year-old friend, both college students, not from Pune, had gone to the table point of the Bopdev Ghat on a motorcycle on October 3, 2024.",
    "At around 11 pm, three men came to the spot on their bikes and allegedly threatened them with sharp weapons and robbed their valuables. The accused allegedly tied the woman’s friend with his shirt and belt, then dragged her to an isolated area and gangraped her."
]

source_url = 'https://indianexpress.com/article-url'

# Field extraction
crime_type = 'Rape'  # or 'Gangrape' based on keywords
if re.search(r'gangrape', ' '.join(paragraphs), re.IGNORECASE):
    crime_type = 'Gangrape'

location = 'Bopdev Ghat, Pune'
latitude = 18.4247  # Ideally, use geocoding API here
longitude = 73.8576

# Extract date & time
incident_date = datetime(2024, 10, 3, 23, 0, 0)  # Oct 3, 2024, 11 PM

description = ' '.join(paragraphs)[:500]  # Truncate if too long

# Severity scoring
severity_map = {'Gangrape': 5, 'Rape': 4, 'Molestation': 3, 'Harassment': 2}
severity = severity_map.get(crime_type, 1)

# Prepare insert data
crime_data = {
    'crime_type': crime_type,
    'location': location,
    'latitude': latitude,
    'longitude': longitude,
    'datetime': incident_date,
    'description': description,
    'severity': severity,
    'source': source_url
}

# Insert into DB
try:
    with engine.begin() as conn:
        conn.execute(sqlalchemy.text("""
            INSERT INTO crimes (crime_type, location, latitude, longitude, datetime, description, severity, source)
            VALUES (:crime_type, :location, :latitude, :longitude, :datetime, :description, :severity, :source)
        """), crime_data)
    print("✅ Data inserted successfully!")
except Exception as e:
    print("❌ Error inserting data:", e)


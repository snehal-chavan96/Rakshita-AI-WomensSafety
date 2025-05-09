import requests
from bs4 import BeautifulSoup
import sqlalchemy
from datetime import datetime

# PostgreSQL connection
engine = sqlalchemy.create_engine('postgresql://postgres:root@localhost/rakshita_db')

# Example list of article URLs
article_urls = [
    "https://punemirror.com/pune/crime/pune-crime-news-three-booked-for-harassing-woman-in-vishrantwadi/cid1746090363.htm",
    # Add more URLs here
]

# Prepare list for bulk insert
crime_records = []

for url in article_urls:
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Failed to fetch {url}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # ---- Extract all headings ----
        page_heading = soup.find(class_='page-heading')
        page_description = soup.find(class_='page-description')
        headings_text = ''
        if page_heading:
            headings_text += page_heading.get_text(strip=True) + ' '
        if page_description:
            headings_text += page_description.get_text(strip=True) + ' '

        # ---- Extract all content in div.block-detail-body ----
        block_body = soup.find('div', class_='block-detail-body')
        div_text = ''
        p_text = ''
        heading_inside_div = ''

        if block_body:
            # All <div> tags inside
            divs = block_body.find_all('div')
            div_text = ' '.join([div.get_text(strip=True) for div in divs])

            # All <p> tags inside
            ps = block_body.find_all('p')
            p_text = ' '.join([p.get_text(strip=True) for p in ps])

            # All heading tags (h1, h2, h3, etc.) inside
            headings = block_body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            heading_inside_div = ' '.join([h.get_text(strip=True) for h in headings])

        # Combine all content
        full_content = f"{headings_text} {heading_inside_div} {p_text} {div_text}"

            # Define keyword categories with weights
        keyword_weights = {
            3: ['murder', 'homicide', 'killing', 'manslaughter', 'brutal', 'lynching'],
            2: ['rape', 'molestation', 'sexual assault', 'gangrape', 'child abuse', 'sexual harassment', 'exploitation'],
            1: ['assault', 'attack', 'acid attack', 'violence', 'beating', 'battery', 'physical abuse',
                'kidnapping', 'abduction', 'blackmail', 'threats', 'intimidation', 'extortion', 'stalking',
                'harassment', 'eve-teasing', 'cyberbullying', 'online abuse', 'domestic violence', 'dowry', 'trafficking']
        }

        total_score = 0
        content_lower = full_content.lower()

        for weight, keywords in keyword_weights.items():
            for keyword in keywords:
                if keyword in content_lower:
                    total_score += weight




        # Example metadata
        crime_type = full_content[:255]  # Truncate to fit varchar(255) if needed
        location = 'Pune, India'
        latitude = 18.5247
        longitude = 73.8576
        datetime_of_crime = datetime.now()
        # Map total_score to severity 1–5
        if total_score >= 8:
            severity = 5
        elif total_score >= 6:
            severity = 4
        elif total_score >= 4:
            severity = 3
        elif total_score >= 2:
            severity = 2
        else:
            severity = 1
        source = url

        crime_record = {
            'crime_type': crime_type,
            'location': location,
            'latitude': latitude,
            'longitude': longitude,
            'datetime': datetime_of_crime,
            'severity': severity,
            'source': source
        }

        crime_records.append(crime_record)
        print(f"✅ Prepared record from {url}")

    except Exception as e:
        print(f"❌ Error processing {url}: {e}")

# Bulk insert into database
if crime_records:
    try:
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text("""
                INSERT INTO crimes (crime_type, location, latitude, longitude, datetime, severity, source)
                VALUES (:crime_type, :location, :latitude, :longitude, :datetime, :severity, :source)
            """), crime_records)
        print(f"✅ Successfully inserted {len(crime_records)} records into the database!")
    except Exception as e:
        print("❌ Error inserting data:", e)
else:
    print("⚠ No records to insert.")


# ***********************************
# import requests
# from bs4 import BeautifulSoup
# import sqlalchemy
# from datetime import datetime

# # PostgreSQL connection
# engine = sqlalchemy.create_engine('postgresql://postgres:root@localhost/rakshita_db')

# # Example list of article URLs (you can expand this)
# article_urls = [
#     "https://indianexpress.com/article/cities/pune/pune-crime-against-women-rise-2024-9795723/",
#     # Add more URLs here
# ]

# # Prepare list for bulk insert
# crime_records = []

# for url in article_urls:
#     try:
#         response = requests.get(url)
#         if response.status_code != 200:
#             print(f"❌ Failed to fetch {url}")
#             continue

#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract headline or title
#         h1 = soup.find('h1').get_text(strip=True)

#         # Extract paragraphs
#         content_div = soup.find(id='pcl-full-content')
#         if not content_div:
#             print(f"⚠ No content found for {url}")
#             continue

#         paragraphs = [p.get_text(strip=True) for p in content_div.find_all('p')]
#         # description = ' '.join(paragraphs)

#         # Example data (you can improve by parsing specific details)
#         crime_type = 'Rape, Molestation' if 'Rape' in h1 or 'Molestation' in h1 else 'Other'
#         location = 'Pune, India'
#         latitude = 18.5247
#         longitude = 73.8576
#         datetime_of_crime = datetime.now()  # or extract from article if available
#         severity = 5  # Adjust logic as needed
#         source = url

#         crime_record = {
#             'crime_type': crime_type,
#             'location': location,
#             'latitude': latitude,
#             'longitude': longitude,
#             'datetime': datetime_of_crime,
#             'severity': severity,
#             'source': source
#         }

#         crime_records.append(crime_record)
#         print(f"✅ Prepared record from {url}")

#     except Exception as e:
#         print(f"❌ Error processing {url}: {e}")

# # Bulk insert into database
# if crime_records:
#     try:
#         with engine.begin() as conn:
#             conn.execute(sqlalchemy.text("""
#                 INSERT INTO crimes (crime_type, location, latitude, longitude, datetime, severity, source)
#                 VALUES (:crime_type, :location, :latitude, :longitude, :datetime, :severity, :source)
#             """), crime_records)
#         print(f"✅ Successfully inserted {len(crime_records)} records into the database!")
#     except Exception as e:
#         print("❌ Error inserting data:", e)
# else:
#     print("⚠ No records to insert.")

# ***********************************

# import requests
# from bs4 import BeautifulSoup

# url = 'https://indianexpress.com/article/cities/pune/pune-crime-against-women-rise-2024-9795723/'

# # Fetch the page
# response = requests.get(url)
# if response.status_code != 200:
#     print(f"Failed to fetch page: {response.status_code}")
#     exit()

# # Parse HTML
# soup = BeautifulSoup(response.text, 'html.parser')

# # Get <h1> tag
# h1_tag = soup.find('h1', id='main-heading-article')
# if h1_tag:
#     print(f"H1 headline:\n{h1_tag.get_text()}\n")
# else:
#     print("H1 headline not found.\n")

# # Get <h2> tag just after <h1>
# h2_tag = h1_tag.find_next('h2') if h1_tag else None
# if h2_tag:
#     print(f"H2 after H1:\n{h2_tag.get_text()}\n")
# else:
#     print("No H2 tag found after H1.\n")

# # Get all <p> tags inside the target <div>
# content_div = soup.find('div', id='pcl-full-content', class_='story_details')
# if content_div:
#     paragraphs = content_div.find_all('p')
#     print("Paragraphs inside #pcl-full-content:\n")
#     for i, p in enumerate(paragraphs, start=1):
#         print(f"{i}. {p.get_text()}\n")
# else:
#     print("Content div with id 'pcl-full-content' not found.")



# import requests
# from bs4 import BeautifulSoup
# import sqlalchemy
# from datetime import datetime

# # PostgreSQL connection
# engine = sqlalchemy.create_engine('postgresql://postgres:root@localhost/rakshita_db')

# # Target website (replace with the actual URL)
# url = "https://indianexpress.com/article/cities/pune/pune-crime-against-women-rise-2024-9795723/"

# # Send GET request
# response = requests.get(url)
# if response.status_code != 200:
#     raise Exception(f"Failed to fetch page: {response.status_code}")

# # Parse HTML
# soup = BeautifulSoup(response.text, 'html.parser')

# # Get headline
# h1 = soup.find('h1').get_text(strip=True)

# # Get content paragraphs
# content_div = soup.find(id='pcl-full-content')
# paragraphs = [p.get_text(strip=True) for p in content_div.find_all('p')]

# # Combine all text for description
# # description = ' '.join(paragraphs)t

# # ===== Fill in extracted details =====
# crime_type = 'Rape, Molestation'  # Based on article topic
# location = 'Pune, India'
# latitude = 18.5247
# longitude = 73.8576
# datetime_of_crime = datetime(2024, 10, 3, 23, 0, 0)  # Example: Bopdev Ghat case time, adjust as needed
# severity = 5  # Arbitrary scale 1–5; you can adjust or set rules later
# source = url

# crime_data = {
#     'crime_type': crime_type,
#     'location': location,
#     'latitude': latitude,
#     'longitude': longitude,
#     'datetime': datetime_of_crime,
#     'severity': severity,
#     'source': source
# }

# # Insert into database
# try:
#     with engine.begin() as conn:
#         conn.execute(sqlalchemy.text("""
#             INSERT INTO crimes (crime_type, location, latitude, longitude, datetime, severity, source)
#             VALUES (:crime_type, :location, :latitude, :longitude, :datetime, :severity, :source)
#         """), crime_data)
#     print("✅ Data inserted successfully!")
# except Exception as e:
#     print("❌ Error inserting data:", e)

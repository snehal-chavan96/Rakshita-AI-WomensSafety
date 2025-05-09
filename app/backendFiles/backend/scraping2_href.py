import requests
from bs4 import BeautifulSoup
import sqlalchemy
from datetime import datetime
from geopy.geocoders import Nominatim

# PostgreSQL connection
engine = sqlalchemy.create_engine('postgresql://postgres:root@localhost/rakshita_db')

# Define keyword weights for severity calculation
keyword_weights = {
    5: ['murder', 'homicide', 'killing', 'manslaughter', 'brutal', 'lynching'],
    4: ['rape', 'molestation', 'sexual assault', 'gangrape', 'child abuse', 'sexual harassment', 'exploitation'],
    3: ['assault', 'acid attack', 'violence', 'beating', 'battery', 'physical abuse', 'kidnapping'],
    2: ['blackmail', 'threats', 'intimidation', 'extortion', 'stalking', 'harassment', 'eve-teasing'],
    1: ['cyberbullying', 'online abuse', 'domestic violence', 'dowry', 'trafficking']
}

crime_type_keywords = {
    'Sexual Crime': ['rape', 'molestation', 'sexual assault', 'gangrape', 'child abuse', 'sexual harassment'],
    'Violence': ['murder', 'homicide', 'beating', 'battery', 'physical abuse', 'acid attack'],
    'Harassment': ['harassment', 'eve-teasing', 'cyberbullying', 'online abuse', 'stalking'],
    'Abduction': ['kidnapping', 'abduction'],
    'Domestic Violence': ['domestic violence', 'dowry', 'physical abuse'],
    'Trafficking': ['trafficking', 'exploitation'],
    'Other': ['fraud', 'theft', 'robbery', 'vandalism', 'burglary']
}

# Expanded women-related keywords
relevant_keywords = [
    'woman', 'women', 'girl', 'minor', 'female', 'wife', 'daughter', 
    'rape', 'molestation', 'sexual assault', 'domestic violence', 
    'acid attack', 'eve-teasing', 'dowry', 'harassment', 'abduction', 'trafficking'
]

# Expanded woman-related terms
woman_terms = [
    'woman', 'women', 'girl', 'minor', 'female', 'wife', 'daughter', 'sister', 'mother', 
    'aunt', 'grandmother', 'niece', 'lady', 'female employee', 'female student', 
    'schoolgirl', 'college girl', 'female passenger', 'bride', 'fiancée'
]

# Expanded women-focused crime keywords
women_crime_keywords = [
    'rape', 'molestation', 'sexual assault', 'gangrape', 'child abuse', 'sexual harassment', 
    'acid attack', 'domestic violence', 'dowry harassment', 'dowry death', 'eve-teasing', 
    'stalking', 'cyberstalking', 'revenge porn', 'sextortion', 'trafficking', 'bride trafficking', 
    'honour killing', 'forced marriage', 'child marriage', 'female foeticide', 'female infanticide', 
    'female genital mutilation', 'forced prostitution', 'forced surrogacy', 'obscene','molested'
]

pune_areas = [
    'Aundh', 'Baner', 'Balewadi', 'Bavdhan', 'Pashan', 'Kothrud', 'Karve Nagar', 'Sinhagad Road', 
    'Warje', 'Wakad', 'Hinjewadi', 'Pimple Saudagar', 'Pimple Gurav', 'Pimple Nilakh', 
    'Chinchwad', 'Pimpri', 'Nigdi', 'Akurdi', 'Ravet', 'Thergaon', 'Kalewadi', 'Sangvi', 
    'Dapodi', 'Bhosari', 'Alandi', 'Moshi', 'Chakan', 'Talegaon', 'Dehu Road', 'Vadgaon', 
    'Vishrantwadi', 'Yerwada', 'Kalyani Nagar', 'Koregaon Park', 'Mundhwa', 'Magarpatta', 
    'Hadapsar', 'Fursungi', 'Kharadi', 'Viman Nagar', 'Lohegaon', 'Dhanori', 'Tingre Nagar', 
    'Chandan Nagar', 'Kondhwa', 'Wanowrie', 'NIBM', 'Undri', 'Pisoli', 'Bibvewadi', 'Sahakar Nagar', 
    'Satara Road', 'Mukund Nagar', 'Swargate', 'Shivajinagar', 'Deccan', 'FC Road', 'JM Road', 
    'Camp', 'MG Road', 'Boat Club Road', 'Parvati', 'Budhwar Peth', 'Shaniwar Peth', 
    'Sadashiv Peth', 'Narayan Peth', 'Raviwar Peth', 'Somwar Peth', 'Guruwar Peth', 'Kasba Peth', 
    'Ghorpadi', 'Fatima Nagar', 'Salunke Vihar', 'Wanwadi', 'Market Yard', 'Gultekdi', 
    'Katraj', 'Ambegaon', 'Dhankawadi', 'Bharati Vidyapeeth', 'Sinhgad College', 'Pune Station'
]



base_url = "https://punemirror.com"

# Updated is_relevant_article function
def is_relevant_article(content):
    content_lower = content.lower()

    # Check for general woman-related terms
    has_woman_term = any(term in content_lower for term in woman_terms)

    # Check for women-specific crime keywords
    has_women_crime_term = any(term in content_lower for term in women_crime_keywords)

    # Optional debug logging
    if not has_woman_term:
        print("⚠ Skipping: No woman term detected.")
    if not has_women_crime_term:
        print("⚠ Skipping: No women-specific crime term detected.")

    return has_woman_term and has_women_crime_term


def calculate_severity(content):
    total_score = 0
    content_lower = content.lower()
    for weight, keywords in keyword_weights.items():
        for keyword in keywords:
            if keyword in content_lower:
                total_score += weight
    if total_score >= 12:
        return 5
    elif total_score >= 9:
        return 4
    elif total_score >= 6:
        return 3
    elif total_score >= 3:
        return 2
    else:
        return 1

def determine_crime_type(content):
    content_lower = content.lower()
    for crime_type, keywords in crime_type_keywords.items():
        if any(keyword in content_lower for keyword in keywords):
            return crime_type
    return 'Other'

def get_lat_long_from_location(location_name):
    geolocator = Nominatim(user_agent="crime_scraper")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    return None, None

def extract_area_from_content(content, area_list): 
    for area in area_list:
        if area.lower() in content.lower():
            return area
    return None


def scrape_article_detail(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f" Failed to fetch {url}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.find('h1').get_text(strip=True)
    
    # Change the class from 'block-detail' to 'block-detail_body' here
    content_div = soup.find('div', {'class': 'block-detail_body'})
    if not content_div:
        print(f" No content found for {url}")
        return None

    # Extracting paragraphs and headings within the correct div
    paragraphs = [p.get_text(strip=True) for p in content_div.find_all('p')]
    headings = [heading.get_text(strip=True) for heading in content_div.find_all(['h2', 'h3', 'h4'])]
    full_content = ' '.join(paragraphs + headings)

    severity = calculate_severity(full_content)
    crime_type = determine_crime_type(full_content)

    # Attempt to extract location from title (optional improvement)
    matched_area = extract_area_from_content(h1 + ' ' + full_content, pune_areas)
    if matched_area:
        location = f"{matched_area}, Pune, India"
    else:
        location = "Pune, India"  # fallback

    latitude, longitude = get_lat_long_from_location(location)


    # Try to get publication date (if available)
    pub_date = datetime.now()
    date_tag = soup.find('span', {'class': 'date'})
    if date_tag:
        try:
            pub_date = datetime.strptime(date_tag.get_text(strip=True), '%b %d, %Y')
        except Exception:
            pass

    return {
        'title': h1,
        'content': full_content,
        'url': url,
        'severity': severity,
        'crime_type': crime_type,
        'location': location,
        'latitude': latitude,
        'longitude': longitude,
        'datetime': pub_date
    }

def get_article_links(base_url):
    url = f'{base_url}/pune/crime/?page=3'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    article_container = soup.find('div', id='article-container')
    if not article_container:
        print('  No article container found.')
        return []

    links = []
    wraps = article_container.find_all('div', class_='wrap')
    for wrap in wraps:
        col_md_8 = wrap.find('div', class_='col-md-8')
        if col_md_8:
            link_tag = col_md_8.find('a', href=True)
            if link_tag:
                article_href = link_tag['href']
                # Make sure to attach ONLY to base domain
                if not article_href.startswith('http'):
                    article_url = base_url + article_href
                else:
                    article_url = article_href
                links.append(article_url)

    return links

def url_exists_in_db(url):
    with engine.begin() as conn:
        result = conn.execute(sqlalchemy.text("SELECT 1 FROM crimes WHERE source = :url"), {'url': url})
        return result.first() is not None

crime_records = []

# Only scrape the first page
page_url = f"{base_url}/pune/crime/?page=1"
article_links = get_article_links(base_url)
for url in article_links:
    if url_exists_in_db(url):
        print(f"⚠ Skipping duplicate: {url}")
        continue
    article_data = scrape_article_detail(url)
    if article_data and is_relevant_article(article_data['content']):
        crime_record = {
            'crime_type': article_data['crime_type'],
            'location': article_data['location'],
            'latitude': article_data['latitude'],
            'longitude': article_data['longitude'],
            'datetime': article_data['datetime'],
            'severity': article_data['severity'],
            'source': article_data['url']
        }
        crime_records.append(crime_record)
        print(f" Scraped relevant article: {url}")
    else:
        print(f" Irrelevant article, skipped: {url}")

# Insert into DB
if crime_records:
    try:
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text("""
                INSERT INTO crimes (crime_type, location, latitude, longitude, datetime, severity, source)
                VALUES (:crime_type, :location, :latitude, :longitude, :datetime, :severity, :source)
            """), crime_records)
        print(f"✅ Inserted {len(crime_records)} new records into the database!")
    except Exception as e:
        print(" Error inserting data:", e)
else:
    print(" No new relevant records found.")

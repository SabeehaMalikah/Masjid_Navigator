import os
import json
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_PLACES_API_KEY")
db_url = os.getenv("DATABASE_URL")


def fetch_mosques():
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type" : "application/json",
        "X-Goog-Api-Key" : api_key,
        "X-Goog-FieldMask" : "places.id,places.displayName,places.formattedAddress,places.location,places.rating,places.reviews"
    }

    body = {
        "textQuery" : "Mosques in Brooklyn"
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("places", [])
    else:
        print(response.status_code)
        print(response.text)
        return dict()

def build_database(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS mosque (
        id BIGSERIAL PRIMARY KEY,
        google_places_id VARCHAR(50),
        name VARCHAR(250),
        address VARCHAR(250),
        latitude FLOAT,
        longitude FLOAT,
        rating FLOAT,
        reviews JSON
    );
    ''')


def populate_database(data, cursor):
    query = ''' INSERT INTO mosque(google_places_id, name, address, latitude, longitude, rating, reviews) 
    VALUES(%s, %s, %s, %s, %s, %s, %s);
    '''

    for entry in data:
        google_places_id = entry.get("id")
        name = entry.get("displayName", {}).get("text", "")
        address = entry.get("formattedAddress", "")
        latitude = entry.get("location", {}).get("latitude", "")
        longitude = entry.get("location", {}).get("longitude", "")
        rating = entry.get("rating", {})
        reviews = entry.get("reviews", [])
        reviews = json.dumps(reviews)

        cursor.execute(query, (
            google_places_id,
            name,
            address,
            latitude,
            longitude,
            rating,
            reviews
        ))


# main
mosques_dict = fetch_mosques()
connection = psycopg2.connect(db_url)
cursor = connection.cursor()
build_database(cursor)
populate_database(mosques_dict, cursor)
connection.commit()
cursor.close()
connection.close()

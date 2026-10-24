import os
import time
import json
import psycopg2
import requests
from dotenv import load_dotenv

# Script to build and populate the mosque table in the database.

load_dotenv()

api_key = os.getenv("GOOGLE_PLACES_API_KEY")
db_url = os.getenv("DATABASE_URL")

def load_neighborhoods():
    '''
    Loads the list of neighborhoods from the "nyc_neighborhoods.txt" file.
    
    Each line in the file represents a neighborhood.

    returns:
        list: A list of neighborhood names.
    '''
    
    neighborhoods = []
    with open("nyc_neighborhoods.txt", "r") as file:
        for line in file:
            neighborhoods.append(line.strip())
    return neighborhoods


def fetch_mosques(neighborhoods):
    ''' 
    Fetches mosques from the Google Places API for the given neighborhoods.
    
    parameters:
        neighborhoods (list): A list of neighborhood names to search for mosques.

    returns:
        list: A list of mosque entries retrieved from the API.
    '''

    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type" : "application/json",
        "X-Goog-Api-Key" : api_key,
        "X-Goog-FieldMask" : "places.id,places.displayName,places.formattedAddress,places.location,places.rating,places.reviews"
    }

    mosques = []

    for n in neighborhoods:
        next_page_token = None
        while True:
            payload = {
                "textQuery" : f"Mosques in {n} NY"
            }

            if next_page_token != None:
                payload["pageToken"] = next_page_token

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                print(response.status_code)
                print(response.text)
                break
            else:
                data = response.json()
                places =  data.get("places", [])
                mosques.extend(places)

                next_page_token = data.get("nextPageToken")

                if next_page_token == None:
                    break

                time.sleep(2)

    return mosques
     

def build_database(cursor):
    ''' 
    Creates the mosque table in the database if it does not already exist.
    
    The table includes columns for the mosque ID, Google Places ID, name, address,
    latitude, longitude, rating, and reviews.

    parameters:
        cursor (psycopg2.cursor): The database cursor used to execute SQL commands.

    returns:
        None
    '''

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

    cursor.execute('''ALTER TABLE mosque ADD CONSTRAINT unique_google_places_id UNIQUE (google_places_id);''')


def populate_database(data, cursor):
    '''
    Populates the mosque table in the database with the provided data.
    
    The function inserts each mosque entry into the mosque table, ensuring that
    duplicate entries based on the Google Places ID are ignored.

    parameters:
        data (list): A list of mosque entries to be inserted into the database.
        cursor (psycopg2.cursor): The database cursor used to execute SQL commands.

    returns:
        None
    '''

    query = ''' INSERT INTO mosque(google_places_id, name, address, latitude, longitude, rating, reviews) 
    VALUES(%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (google_places_id) DO NOTHING;
    '''

    for entry in data:
        google_places_id = entry.get("id")
        display_name = entry.get("displayName", {})
        name = display_name.get("text") if isinstance(display_name, dict) else None
        address = entry.get("formattedAddress", "")
        location = entry.get("location", {})
        latitude = location.get("latitude") if isinstance(location, dict) else None
        longitude = location.get("longitude") if isinstance(location, dict) else None
        rating = entry.get("rating")
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


def main():
    '''
    Main function to build and populate the mosque table in the database.
    '''
    neighborhoods_list = load_neighborhoods()
    mosques_dict = fetch_mosques(neighborhoods_list)
    connection = psycopg2.connect(
        db_url,
        options="-c client_encoding=utf8"
    )
    connection.set_client_encoding('UTF8')
    cursor = connection.cursor()
    build_database(cursor)
    populate_database(mosques_dict, cursor)
    connection.commit()
    cursor.close()
    connection.close()

main()
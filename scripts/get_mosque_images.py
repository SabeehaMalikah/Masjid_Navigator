import requests
import os
import time
import psycopg2
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GOOGLE_PLACES_API_KEY")
db_url = os.getenv("DATABASE_URL")

def get_mosque_ids(cursor):
    cursor.execute('''SELECT google_places_id FROM mosque''')
    return [row[0] for row in cursor.fetchall()]

def download_photo(mosque_id):
    url = f"https://places.googleapis.com/v1/places/{mosque_id}"
    headers = {
    "X-Goog-Api-Key": api_key,
    "X-Goog-FieldMask": "photos"
    }
    
    response = requests.get(url, headers=headers).json()
    photos = response.get("photos", [])
    print("Photo acquired!")

    if photos:
        photo_name = photos[0]["name"]
        media_url = f"https://places.googleapis.com/v1/{photo_name}/media"
        params = {
            "maxWidthPx": 400,
            "key": api_key
        }

        img = requests.get(media_url, params=params)
        if img.status_code == 200:
            with open(f"public/images/mosques/{mosque_id}.jpg", "wb") as f:
                f.write(img.content)
            print("Image downloaded!")

def main():
    connection = psycopg2.connect(
        db_url,
        options="-c client_encoding=utf8"
    )
    connection.set_client_encoding('UTF8')
    cursor = connection.cursor()

    mosque_ids_list = get_mosque_ids(cursor)
    for id in mosque_ids_list:
        download_photo(id)
        time.sleep(0.1)

    cursor.close()
    connection.close()

main()

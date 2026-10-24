import requests
import os
from dotenv import load_dotenv

# Script to test the Google Places API for fetching mosque information in Brooklyn, NY.

load_dotenv()

api_key = os.getenv("GOOGLE_PLACES_API_KEY")

def find_mosques():
    '''
    Fetches a list of mosques in Brooklyn, NY using the Google Places API.

    returns:
        list: A list of mosque entries retrieved from the API.
    '''
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type" : "application/json",
        "X-Goog-Api-Key" : api_key,
        "X-Goog-FieldMask" : "places.displayName,places.formattedAddress,places.location,places.reviews"
    }

    body = {
        "textQuery" : "Mosques in Brooklyn, NY"
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("places", [])
    else:
        print(response.status_code)
        print(response.text)
        return dict()

def pretty_print(mosques_dict):
    '''
    Pretty prints the information of mosques and their reviews.

    parameters:
        mosques_dict (list): A list of mosque entries to be printed.

    returns:
        None
    '''
    def print_info(name, address, latitude, longitude):
        '''
        Prints the basic information of a mosque.

        parameters:
            name (str): The name of the mosque.
            address (str): The address of the mosque.
            latitude (float): The latitude of the mosque's location.
            longitude (float): The longitude of the mosque's location.

        returns:
            None
        '''
        print(
            f"{name}\n" \
            f"Address: {address}\n" \
            f"Location: {latitude, longitude}\n"
        )

    def print_review(rating, time, date, author, text):
        '''
        Prints the information of a single review.

        parameters:
            rating (str): The rating of the review.
            time (str): The relative publish time of the review.
            date (str): The publish date of the review.
            author (str): The author of the review.
            text (str): The text content of the review.

        returns:
            None
        '''
        print(
            f"Author: {author}\n" \
            f"Time: {time}\n" \
            f"Date: {date}\n" \
            f"Rating: {rating} 🌟\n" \
        )
        if text:
            print(f"Review: \n{text}\n")

        print("_________________________________________________")

    if len(mosques_dict) != 0:
        for mosque in mosques_dict:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            name = mosque.get("displayName", {}).get("text", "")
            address = mosque.get("formattedAddress", "")
            latitude = mosque.get("location", {}).get("latitude", "")
            longitude = mosque.get("location", {}).get("longitude", "")
            print_info(name, address, latitude, longitude)

            reviews = mosque.get("reviews", {})
            print("\nReviews")
            print("_________________________________________________")
            for review in reviews:
                rating = review.get("rating", "")
                time = review.get("relativePublishTimeDescription", "")
                date = review.get("publishTime", "")
                author = review.get("authorAttribution", {}).get("displayName")
                text = review.get("text", {}).get("text", "")
                print_review(rating, time, date, author, text)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print()
            print()

    


def main():
    '''
    Main function to test the API by fetching and pretty printing mosque information.
    '''
    print("Welcome to Masjid Navigator!")
    result = find_mosques()
    pretty_print(result[:2])

main()

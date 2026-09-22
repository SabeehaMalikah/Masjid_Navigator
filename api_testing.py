import requests

def find_mosques():
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type" : "application/json",
        "X-Goog-Api-Key" : "AIzaSyBMSDTuVkHUjxCLrBQFM5KsswqnJXAzLbQ",
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
    def print_info(name, address, latitude, longitude):
        print(
            f"{name}\n" \
            f"Address: {address}\n" \
            f"Location: {latitude, longitude}\n"
        )

    def print_review(rating, time, date, author, text):
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
    result = find_mosques()
    pretty_print(result[:2])
main()

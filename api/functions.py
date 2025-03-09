import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load API Key
SERPER_API_KEY = os.getenv('SERPER_API_KEY')

def get_location_info(destination):
    """
    Fetches latitude and longitude for a given destination using Serper.dev API.

    Args:
        destination (str): The name of the location to search.

    Returns:
        dict: A dictionary containing title, address, latitude, longitude, rating, and category.
    """
    url = "https://google.serper.dev/places"

    payload = json.dumps({"q": destination})
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json()
            places = data.get("places", [])

            if not places:
                return {"error": "No results found"}

            first_place = places[0]  # Extracting first place details
            
            return {
                "title": first_place.get("title"),
                "address": first_place.get("address"),
                "latitude": first_place.get("latitude"),
                "longitude": first_place.get("longitude"),
                "rating": first_place.get("rating"),
                "category": first_place.get("category")
            }

        elif response.status_code == 403:
            return {"error": "Access forbidden. Ensure your API key is valid."}

        else:
            return {"error": f"Request failed with status code {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
from langchain.tools import tool
from tools.maps import geocode_place

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")

# =====================================================
# Category Mapping
# =====================================================

CATEGORY_MAP = {
    "tourism": "Tourist Attraction",
    "tourism.attraction": "Tourist Attraction",
    "tourism.sights": "Tourist Attraction",
    "museum": "Museum",
    "historic": "Historic Site",
    "religion": "Religious Site",
    "park": "Park",
    "beach": "Beach",
    "viewpoint": "Viewpoint",
    "entertainment": "Entertainment",
    "natural": "Nature"
}

# =====================================================
# Attractions Tool
# =====================================================

@tool
def get_attractions(city: str) -> str:
    """
    Get the top tourist attractions in a city.

    Returns:
    - Attraction Name
    - Category
    - Address
    - Distance
    """

    # -------------------------------------------------
    # Validate API Key
    # -------------------------------------------------

    if not API_KEY:
        return "Geoapify API key is missing."

    # -------------------------------------------------
    # Get Coordinates
    # -------------------------------------------------

    location = geocode_place(city)

    if not location:
        return f"Unable to locate '{city}'."

    latitude = location["latitude"]
    longitude = location["longitude"]

    # -------------------------------------------------
    # Geoapify Places API
    # -------------------------------------------------

    url = "https://api.geoapify.com/v2/places"

    params = {
        "categories": "tourism",
        "filter": f"circle:{longitude},{latitude},10000",
        "bias": f"proximity:{longitude},{latitude}",
        "limit": 20,
        "apiKey": API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        places = data.get("features", [])

        if not places:
            return f"No tourist attractions found in {city.title()}."

        results = []
        seen = set()

        # -------------------------------------------------
        # Process Attractions
        # -------------------------------------------------

        for place in places:

            properties = place.get("properties", {})

            # -----------------------------------------
            # Name
            # -----------------------------------------

            name = properties.get("name", "").strip()

            if not name:
                continue

            if name.lower() in {
                "unknown",
                "tourism",
                "attraction"
            }:
                continue

            # -----------------------------------------
            # Remove Duplicates
            # -----------------------------------------

            key = " ".join(name.lower().split())

            if key in seen:
                continue

            seen.add(key)

            # -----------------------------------------
            # Address
            # -----------------------------------------

            address = (
                properties.get("formatted")
                or properties.get("address_line2")
                or "Address unavailable"
            )

            # -----------------------------------------
            # Distance
            # -----------------------------------------

            distance = properties.get("distance", 0)

            if distance >= 1000:
                distance_text = f"{distance / 1000:.1f} km"
            else:
                distance_text = f"{distance} m"

            # -----------------------------------------
            # Category
            # -----------------------------------------

            category = "Tourist Attraction"

            for item in properties.get("categories", []):

                if item in CATEGORY_MAP:
                    category = CATEGORY_MAP[item]
                    break

            results.append({
                "name": name,
                "category": category,
                "address": address,
                "distance": distance,
                "distance_text": distance_text
            })

        if not results:
            return f"No tourist attractions found in {city.title()}."

        # -------------------------------------------------
        # Sort by Distance (Nearest First)
        # -------------------------------------------------

        results.sort(
            key=lambda x: x["distance"]
        )

        # Keep only Top 10

        results = results[:10]

        # -------------------------------------------------
        # Output
        # -------------------------------------------------

        output = [
            f"🏛️ Top Tourist Attractions in {city.title()}",
            f"Found {len(results)} attractions",
            ""
        ]

        for index, place in enumerate(results, start=1):

            output.append(
                f"""{index}. {place['name']}
🏷️ Category : {place['category']}
📍 {place['address']}
🚶 Distance : {place['distance_text']}
"""
            )

        return "\n".join(output)

    except requests.exceptions.Timeout:
        return "The attractions service took too long to respond."

    except requests.exceptions.ConnectionError:
        return "Unable to connect to the attractions service."

    except requests.exceptions.HTTPError as e:
        return f"Geoapify returned an HTTP error: {e}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"
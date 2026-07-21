from langchain.tools import tool
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import requests
import os
from dotenv import load_dotenv

load_dotenv()

ORS_API_KEY = os.getenv("OPENROUTESERVICE_API_KEY")

# ==========================================================
# INTERNAL HELPER FUNCTION
# ==========================================================
# This function is NOT a LangChain tool.
# It is used internally to convert a place name into
# latitude and longitude.
#
# Example:
# "Kochi International Airport"
# ->
# {
#     "name": "Cochin International Airport",
#     "latitude": 10.152,
#     "longitude": 76.392
# }
# ==========================================================

geolocator = Nominatim(user_agent="ai_travel_planner")


def geocode_place(place: str):
    """
    Convert a place name into latitude and longitude.

    Returns:
        dict or None
    """

    # Assume India if no country is specified
    if "," not in place:
        place = f"{place}, India"

    try:
        location = geolocator.geocode(place)

        if location is None:
            return None

        return {
            "name": location.address.split(",")[0],
            "display_name": location.address,
            "latitude": location.latitude,
            "longitude": location.longitude
        }

    except Exception:
        return None


# ==========================================================
# LANGCHAIN TOOL
# ==========================================================
# This tool is used by the AI agent.
#
# It:
# 1. Converts origin & destination into coordinates
# 2. Calls OpenRouteService
# 3. Returns distance & travel duration
# ==========================================================

@tool
def get_distance(origin: str, destination: str) -> str:
    """
    Calculate road distance and travel time between two places.
    """

    start = geocode_place(origin)
    end = geocode_place(destination)

    if start is None:
        return f"Could not find location: {origin}"

    if end is None:
        return f"Could not find location: {destination}"

    headers = {
        "Authorization": ORS_API_KEY
    }

    body = {
        "coordinates": [
            [start["longitude"], start["latitude"]],
            [end["longitude"], end["latitude"]]
        ]
    }

    try:

        response = requests.post(
            "https://api.openrouteservice.org/v2/directions/driving-car",
            json=body,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        summary = data["routes"][0]["summary"]

        distance_km = summary["distance"] / 1000
        duration_min = summary["duration"] / 60

        return f"""
🗺️ Route Information

From : {start["name"]}
To   : {end["name"]}

Distance : {distance_km:.2f} km
Duration : {duration_min:.0f} minutes
"""

    except Exception as e:

        # Fallback to straight-line distance

        distance = geodesic(
            (start["latitude"], start["longitude"]),
            (end["latitude"], end["longitude"])
        ).km

        return f"""
🗺️ Route Information

From : {start["name"]}
To   : {end["name"]}

Road route unavailable.

Approximate straight-line distance:
{distance:.2f} km

Error:
{str(e)}
"""
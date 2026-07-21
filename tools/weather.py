from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

# ---------------------------------------
# Load Environment Variables
# ---------------------------------------

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@tool
def get_weather(city: str) -> str:
    """
    Get the current weather information for a city.

    Returns:
    - Weather condition
    - Temperature
    - Feels like temperature
    - Humidity
    - Wind speed
    - Simple travel advice
    """

    if not API_KEY:
        return "OpenWeather API key is not configured."

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            try:
                error = response.json().get("message", "Unknown error")
            except Exception:
                error = "Unknown error"

            return f"Unable to fetch weather for '{city}'. Reason: {error}"

        data = response.json()

        city_name = data.get("name", city.title())

        weather = data["weather"][0]["description"].title()

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        advice = []

        # Temperature Advice

        if temperature >= 35:
            advice.append("🥵 Very hot weather. Stay hydrated and use sunscreen.")

        elif temperature >= 28:
            advice.append("☀️ Warm weather. Wear light clothing.")

        elif temperature >= 20:
            advice.append("😊 Pleasant weather for sightseeing.")

        elif temperature >= 10:
            advice.append("🧥 Carry a light jacket.")

        else:
            advice.append("❄️ Cold weather. Dress warmly.")

        # Weather Condition Advice

        condition = weather.lower()

        if "rain" in condition:
            advice.append("🌧️ Carry an umbrella or raincoat.")

        elif "cloud" in condition:
            advice.append("☁️ Cloudy skies expected.")

        elif "clear" in condition:
            advice.append("🌞 Great weather for outdoor activities.")

        elif "storm" in condition:
            advice.append("⛈️ Avoid outdoor activities if possible.")

        elif "snow" in condition:
            advice.append("❄️ Roads may be slippery. Travel carefully.")

        return f"""
🌦️ Weather Report for {city_name}

Condition     : {weather}
Temperature   : {temperature:.1f}°C
Feels Like    : {feels_like:.1f}°C
Humidity      : {humidity}%
Wind Speed    : {wind_speed:.1f} m/s

Travel Advice:
{chr(10).join(f"- {item}" for item in advice)}
"""

    except requests.exceptions.Timeout:
        return "The weather service took too long to respond."

    except requests.exceptions.ConnectionError:
        return "Unable to connect to the weather service."

    except requests.exceptions.RequestException as e:
        return f"Weather service error: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"
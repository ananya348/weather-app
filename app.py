from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


# --------------------------------
# Weather condition function
# --------------------------------

def get_weather_condition(code):

    conditions = {
        0: ("☀️", "Clear Sky"),

        1: ("🌤️", "Mainly Clear"),
        2: ("⛅", "Partly Cloudy"),
        3: ("☁️", "Overcast"),

        45: ("🌫️", "Fog"),
        48: ("🌫️", "Rime Fog"),

        51: ("🌦️", "Light Drizzle"),
        53: ("🌦️", "Moderate Drizzle"),
        55: ("🌧️", "Dense Drizzle"),

        61: ("🌧️", "Slight Rain"),
        63: ("🌧️", "Moderate Rain"),
        65: ("🌧️", "Heavy Rain"),

        71: ("❄️", "Slight Snow"),
        73: ("❄️", "Moderate Snow"),
        75: ("❄️", "Heavy Snow"),

        80: ("🌦️", "Rain Showers"),
        81: ("🌧️", "Moderate Rain Showers"),
        82: ("⛈️", "Heavy Rain Showers"),

        95: ("⛈️", "Thunderstorm"),
        96: ("⛈️", "Thunderstorm with Hail"),
        99: ("⛈️", "Thunderstorm with Heavy Hail")
    }

    return conditions.get(code, ("🌤️", "Unknown"))


# --------------------------------
# Home page
# --------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------
# Weather API
# --------------------------------

@app.route("/weather")
def weather():

    city = request.args.get("city")

    if not city:
        return jsonify({
            "error": "Please enter a city name."
        }), 400

    try:

        # -----------------------------
        # STEP 1: Geocoding
        # -----------------------------

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_data = geo_response.json()

        if "results" not in geo_data:
            return jsonify({
                "error": "City not found."
            }), 404

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        city_name = location["name"]
        country = location.get("country", "")

        # -----------------------------
        # STEP 2: Weather API
        # -----------------------------

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {

            "latitude": latitude,
            "longitude": longitude,

            # Current weather
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "wind_speed_10m,"
                "weather_code"
            ),

            # 5-day forecast
            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max"
            ),

            "forecast_days": 5,
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_data = weather_response.json()

        # -----------------------------
        # STEP 3: Current weather
        # -----------------------------

        current = weather_data["current"]

        current_icon, current_condition = get_weather_condition(
            current["weather_code"]
        )

        current_weather = {

            "temperature": current["temperature_2m"],

            "feels_like": current["apparent_temperature"],

            "humidity": current["relative_humidity_2m"],

            "wind_speed": current["wind_speed_10m"],

            "condition": current_condition,

            "icon": current_icon
        }

        # -----------------------------
        # STEP 4: 5-day forecast
        # -----------------------------

        daily = weather_data["daily"]

        forecast = []

        for i in range(5):

            icon, condition = get_weather_condition(
                daily["weather_code"][i]
            )

            forecast.append({

                "date": daily["time"][i],

                "max_temp": daily["temperature_2m_max"][i],

                "min_temp": daily["temperature_2m_min"][i],

                "rain_probability":
                    daily["precipitation_probability_max"][i],

                "condition": condition,

                "icon": icon
            })

        # -----------------------------
        # STEP 5: Send data to frontend
        # -----------------------------

        return jsonify({

            "location": city_name,

            "country": country,

            "current": current_weather,

            "forecast": forecast
        })

    except requests.exceptions.RequestException:

        return jsonify({
            "error": "Unable to connect to weather service."
        }), 500

    except Exception as e:

        print(e)

        return jsonify({
            "error": "Something went wrong."
        }), 500


# --------------------------------
# Run Flask
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)
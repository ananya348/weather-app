async function getWeather() {

    const cityInput = document.getElementById("cityInput");

    const city = cityInput.value.trim();

    const loading = document.getElementById("loading");

    const error = document.getElementById("error");


    if (city === "") {

        error.textContent = "❌ Please enter a city name.";

        return;

    }


    loading.style.display = "block";

    error.textContent = "";


    try {

        const response = await fetch(
            `/weather?city=${encodeURIComponent(city)}`
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Unable to get weather."
            );

        }


        displayWeather(data);

    }

    catch (error) {

        console.error(error);

        errorMessage(error.message);

    }

    finally {

        loading.style.display = "none";

    }

}


/* ---------------------------------
   Display Weather
---------------------------------- */

function displayWeather(data) {

    document.getElementById("location").textContent =
        data.location;


    document.getElementById("country").textContent =
        data.country;


    document.getElementById("weatherIcon").textContent =
        data.current.icon;


    document.getElementById("temperature").textContent =
        Math.round(data.current.temperature) + "°C";


    document.getElementById("condition").textContent =
        data.current.condition;


    document.getElementById("feelsLike").textContent =
        Math.round(data.current.feels_like) + "°C";


    document.getElementById("humidity").textContent =
        data.current.humidity + "%";


    document.getElementById("wind").textContent =
        data.current.wind_speed + " km/h";


    displayForecast(data.forecast);

}


/* ---------------------------------
   5 Day Forecast
---------------------------------- */

function displayForecast(forecast) {

    const forecastContainer =
        document.getElementById("forecast");


    forecastContainer.innerHTML = "";


    forecast.forEach(function(day) {

        const date = new Date(day.date);


        const formattedDate =
            date.toLocaleDateString(
                "en-US",
                {
                    weekday: "short",
                    month: "short",
                    day: "numeric"
                }
            );


        const card =
            document.createElement("div");


        card.className = "forecast-card";


        card.innerHTML = `

            <div class="forecast-date">
                ${formattedDate}
            </div>

            <div class="forecast-icon">
                ${day.icon}
            </div>

            <div class="forecast-condition">
                ${day.condition}
            </div>

            <div class="forecast-temp">
                ${Math.round(day.max_temp)}°C /
                ${Math.round(day.min_temp)}°C
            </div>

            <div class="rain">
                🌧️ ${day.rain_probability ?? 0}% rain
            </div>

        `;


        forecastContainer.appendChild(card);

    });

}


/* ---------------------------------
   Error Message
---------------------------------- */

function errorMessage(message) {

    document.getElementById("error").textContent =
        "❌ " + message;

}


/* ---------------------------------
   Search Button
---------------------------------- */

document
    .getElementById("searchButton")
    .addEventListener("click", getWeather);


/* ---------------------------------
   Enter Key
---------------------------------- */

document
    .getElementById("cityInput")
    .addEventListener("keypress", function(event) {

        if (event.key === "Enter") {

            getWeather();

        }

    });
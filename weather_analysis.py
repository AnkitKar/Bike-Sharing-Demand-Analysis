# BIKE SHARING PROJECT
# Weather Analyst by Timothy

import pandas as pd
import matplotlib.pyplot as plt

# First step is to load data to see whether all the data provided is present 
day = pd.read_csv("day.csv")
hour = pd.read_csv("hour.csv")

print("Daily data:", day.shape)
print("Hourly data:", hour.shape)

# The next step is to prepare weather data 
# Convert temperature to Celsius
day["temperature"] = day["temp"] * 41

# Convert humidity to percentage
day["humidity"] = day["hum"] * 100

# Convert wind speed to km/h
day["wind_speed"] = day["windspeed"] * 67

# After preparing the weather variables, we can analyze their correlations with bike rentals
print("\nWEATHER CORRELATIONS")
print(day[
    ["temperature", "humidity", "wind_speed", "cnt"]
].corr()["cnt"])

# Comparing temperature with bike rentals
plt.scatter(day["temperature"], day["cnt"], alpha=0.5)

plt.xlabel("Temperature (Celsius)")
plt.ylabel("Daily Bike Rentals")
plt.title("Temperature vs Bike Rentals")

plt.tight_layout()
plt.show()

# Comparing humidity with bike rentals
plt.scatter(day["humidity"], day["cnt"], alpha=0.5)

plt.xlabel("Humidity (%)")
plt.ylabel("Daily Bike Rentals")
plt.title("Humidity vs Bike Rentals")

plt.tight_layout()
plt.show()

# Comparing wind speed with bike rentals
plt.scatter(day["wind_speed"], day["cnt"], alpha=0.5)

plt.xlabel("Wind Speed (km/h)")
plt.ylabel("Daily Bike Rentals")
plt.title("Wind Speed vs Bike Rentals")

plt.tight_layout()
plt.show()

# Comparing weather conditions with bike rentals
weather_names = {
    1: "Clear",
    2: "Mist/Cloudy",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}

day["weather"] = day["weathersit"].map(weather_names)

weather_demand = day.groupby("weather")["cnt"].mean()

print("\nAVERAGE RENTALS BY WEATHER")
print(weather_demand)

weather_demand.plot(kind="bar")

plt.xlabel("Weather Conditions")
plt.ylabel("Average Daily Rentals")
plt.title("Weather Conditions vs Bike Rentals")

plt.xticks(rotation=20)
plt.tight_layout()
plt.show()

# The next step is to analyze hourly rentals by weather conditions
# Average rentals by hour under different weather conditions
hourly_weather = hour.groupby(
    ["hr", "weathersit"]
)["cnt"].mean().unstack()

# Replace weather numbers with names
hourly_weather = hourly_weather.rename(
    columns=weather_names
)

print("\nHOURLY RENTALS BY WEATHER")
print(hourly_weather)

# Create hourly weather graph
hourly_weather.plot(figsize=(10, 5))

plt.xlabel("Hour of Day")
plt.ylabel("Average Hourly Rentals")
plt.title("Hourly Bike Rentals by Weather Conditions")

plt.xticks(range(0, 24))
plt.legend(title="Weather")
plt.tight_layout()
plt.show()

# Last step is to provide a final summary of the weather analysis
print("\nWEATHER ANALYSIS SUMMARY")

print(
    "Highest average demand weather:",
    weather_demand.idxmax()
)

print("Lowest average demand weather:",
    weather_demand.idxmin())

print("\nWeather analysis completed!")

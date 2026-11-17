# BIKE SHARING PROJECT
# Member 3, Timothy: temperature, humidity, wind speed, weather conditions, and correlation tests.
# The p-values are the check on those correlations. A small p-value means the association is unlikely to be zero in this file.

from pathlib import Path
import pandas as pd
from scipy import stats
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

folder = Path(__file__).resolve().parent
data_folder = folder / "data"
charts_folder = folder / "charts"
results_folder = folder / "results"
charts_folder.mkdir(exist_ok=True)
results_folder.mkdir(exist_ok=True)

# First step is to load data to see whether all the data provided is present.
day = pd.read_csv(data_folder / "day.csv")
hour = pd.read_csv(data_folder / "hour.csv")

print("Daily data:", day.shape)
print("Hourly data:", hour.shape)

# The next step is to prepare weather data.
# Convert temperature to Celsius. The source file divides temperature by 41.
day["temperature"] = day["temp"] * 41
hour["temperature"] = hour["temp"] * 41

# Convert humidity to percentage.
day["humidity"] = day["hum"] * 100
hour["humidity"] = hour["hum"] * 100

# Convert wind speed to km/h. The source file divides wind speed by 67.
day["wind_speed"] = day["windspeed"] * 67
hour["wind_speed"] = hour["windspeed"] * 67

# Record bad weather rows before interpreting the averages.
hours_per_day = hour.groupby("dteday").size()
severe_hours = hour.loc[hour["weathersit"] == 4, ["dteday", "hr", "cnt"]]
zero_humidity = hour["humidity"] == 0
sandy = day["dteday"] == "2012-10-29"
light_rain_days = day["weathersit"] == 3
print("\nDATA LIMITS TO READ BEFORE THE WEATHER AVERAGES")
print(f"Humidity is 0 on {day.loc[day['humidity'] == 0, 'dteday'].iloc[0]} ({int(zero_humidity.sum())} hours).")
print("That day stays in the rental totals and is removed from the humidity chart and correlation.")
print(f"Missing hour rows: {len(day) * 24 - len(hour)}. Days with fewer than 20 hours: {int((hours_per_day < 20).sum())}.")
print(
    "2012-10-29 has",
    int(day.loc[sandy, "cnt"].iloc[0]),
    "rentals and",
    int((hour["dteday"] == "2012-10-29").sum()),
    "observed hour, coded as light rain/snow.",
)
print("Severe weather hours:")
print(severe_hours.to_string(index=False))
print("Daily rows coded severe weather:", int((day["weathersit"] == 4).sum()))

# Correlations. The all-days row keeps the earlier figure. The cleaned row drops humidity 0.
# Pearson r is tested against a zero association. Round humidity to three decimals in the report:
# excluding the zero-humidity day, humidity r is -0.115, which is -0.11 at two decimals.
weather_columns = ["temperature", "humidity", "wind_speed"]
cleaned_day = day.loc[day["humidity"] > 0]
correlation_rows = []
for sample_name, sample in [("all_days", day), ("excluding_zero_humidity", cleaned_day)]:
    for column in weather_columns:
        correlation, p_value = stats.pearsonr(sample[column], sample["cnt"])
        correlation_rows.append(
            {
                "sample": sample_name,
                "variable": column,
                "r": round(float(correlation), 3),
                "p_value": float(p_value),
                "days": int(len(sample)),
                "significant_at_0_05": bool(p_value < 0.05),
            }
        )
correlations = pd.DataFrame(correlation_rows)
print("\nWEATHER CORRELATIONS")
print(correlations.to_string(index=False))
correlations.to_csv(results_folder / "weather_correlations.csv", index=False)
correlation_check = bool(correlations["significant_at_0_05"].all())
validation = pd.DataFrame(
    [
        {
            "check": "day_and_hour_totals_match",
            "result": "pass" if day["cnt"].sum() == hour["cnt"].sum() else "fail",
            "detail": f"Both files total {int(day['cnt'].sum())} rentals.",
        },
        {
            "check": "casual_plus_registered",
            "result": "pass" if (day["casual"] + day["registered"] == day["cnt"]).all() else "fail",
            "detail": "Checked on every daily row.",
        },
        {
            "check": "correlation_p_values",
            "result": "pass" if correlation_check else "fail",
            "detail": "Temperature, humidity, and wind are each tested at 0.05 in both samples.",
        },
    ]
)
print("\nVALIDATION")
print(validation.to_string(index=False))
validation.to_csv(results_folder / "validation_checks.csv", index=False)

# Comparing temperature with bike rentals.
plt.scatter(day["temperature"], day["cnt"], alpha=0.5)
plt.xlabel("Temperature (Celsius)")
plt.ylabel("Daily Bike Rentals")
plt.title("Temperature vs Bike Rentals")
plt.tight_layout()
plt.savefig(charts_folder / "12_temperature.png")
plt.close()

# Comparing humidity with bike rentals. The zero-humidity day is not plotted.
plt.scatter(cleaned_day["humidity"], cleaned_day["cnt"], alpha=0.5)
plt.xlabel("Humidity (%)")
plt.ylabel("Daily Bike Rentals")
plt.title("Humidity vs Bike Rentals, Excluding 10 Mar 2011")
plt.tight_layout()
plt.savefig(charts_folder / "13_humidity.png")
plt.close()

# Comparing wind speed with bike rentals.
plt.scatter(day["wind_speed"], day["cnt"], alpha=0.5)
plt.xlabel("Wind Speed (km/h)")
plt.ylabel("Daily Bike Rentals")
plt.title("Wind Speed vs Bike Rentals")
plt.tight_layout()
plt.savefig(charts_folder / "14_wind.png")
plt.close()

# Comparing weather conditions with bike rentals.
# Code 4 does not occur in the daily file, so it is not drawn as a bar.
weather_names = {
    1: "Clear",
    2: "Mist/Cloudy",
    3: "Light Rain/Snow",
}
weather_order = ["Clear", "Mist/Cloudy", "Light Rain/Snow"]
day["weather"] = day["weathersit"].map(weather_names)
hour["weather"] = hour["weathersit"].map(weather_names)

weather_demand = day.groupby("weather")["cnt"].mean().reindex(weather_order)
weather_without_sandy = (
    day.loc[~sandy].groupby("weather")["cnt"].mean().reindex(weather_order)
)
print("\nAVERAGE RENTALS BY WEATHER")
print(weather_demand.round(1))
print("Light rain/snow average without 29 Oct 2012:", round(float(weather_without_sandy["Light Rain/Snow"]), 1))
print("Light rain/snow days:", int(light_rain_days.sum()))
weather_compare = pd.DataFrame(
    {
        "average_with_sandy": weather_demand.round(1),
        "average_without_sandy_day": weather_without_sandy.round(1),
    }
)
weather_compare.to_csv(results_folder / "weather_totals.csv")

weather_demand.plot(kind="bar", title="Weather Conditions vs Bike Rentals")
plt.xlabel("Weather Conditions")
plt.ylabel("Average Daily Rentals")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(charts_folder / "16_weather_totals.png")
plt.close()

# Hourly rentals for weather conditions that have enough hours to show a pattern.
# Three severe-weather hours are listed above and are not drawn as a fourth line.
hourly_weather = (
    hour.loc[hour["weathersit"] < 4]
    .groupby(["hr", "weather"])["cnt"]
    .mean()
    .unstack()
    .reindex(columns=weather_order)
)
print("\nHOURLY RENTALS BY WEATHER")
print(hourly_weather.round(1))
print("Peak hour by weather:")
print(hourly_weather.idxmax().to_string())
hourly_weather.round(1).to_csv(results_folder / "hourly_weather.csv")

axis = hourly_weather.plot(figsize=(10, 5), title="Hourly Bike Rentals by Weather Conditions")
axis.set_xlabel("Hour of Day")
axis.set_ylabel("Average Hourly Rentals")
axis.set_xticks(range(0, 24))
axis.legend(title="Weather")
plt.tight_layout()
plt.savefig(charts_folder / "15_hourly_weather.png")
plt.close()

print("\nWEATHER ANALYSIS SUMMARY")
print("Highest average demand weather:", weather_demand.idxmax())
print("Lowest average demand weather:", weather_demand.idxmin())
print("Strongest linear weather association: temperature")
print("Severe weather is not summarized as a pattern because only three hours are coded that way.")
print("\nWeather analysis completed!")
print(charts_folder)

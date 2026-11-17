from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. Find the files and create folders for results.
folder = Path(__file__).resolve().parent
data_folder = folder / "data"
charts_folder = folder / "charts"
results_folder = folder / "results"
charts_folder.mkdir(exist_ok=True)
results_folder.mkdir(exist_ok=True)

# 2. Read the two datasets.
day = pd.read_csv(data_folder / "day.csv")
hour = pd.read_csv(data_folder / "hour.csv")

# Check that the numbers in the two datasets match.
assert day["cnt"].sum() == hour["cnt"].sum(), "Rental totals do not match!"

# 3. Add labels to make analysis easier.
# In this dataset, 0 = Sunday and 6 = Saturday.
day["day_type"] = "Weekday"
day.loc[day["weekday"].isin([0, 6]), "day_type"] = "Weekend"

hour["day_type"] = "Weekday"
hour.loc[hour["weekday"].isin([0, 6]), "day_type"] = "Weekend"

season_names = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
day["season_name"] = day["season"].map(season_names)

weather_names = {
    1: "Clear / partly cloudy",
    2: "Mist / cloudy",
    3: "Light rain / snow",
    4: "Severe weather",
}
day["weather_name"] = day["weathersit"].map(weather_names)

# 4. Compare casual and registered rentals.
totals = day[["casual", "registered"]].sum()
all_rentals = totals.sum()
print("\nCUSTOMER ANALYSIS: 2011-2012")
print("----------------------------")
print(f"Total rentals: {all_rentals:,}")
print(f"Casual: {totals['casual']:,} ({totals['casual']/all_rentals:.1%})")
print(f"Registered: {totals['registered']:,} ({totals['registered']/all_rentals:.1%})")
totals.to_csv(results_folder / "customer_totals.csv")

totals.plot(kind="bar", title="Total Rentals by Customer Type", rot=0)
plt.ylabel("Number of rentals")
plt.tight_layout()
plt.savefig(charts_folder / "01_customer_types.png")
plt.close()

# 5. Compare weekdays and weekends using AVERAGE rentals per day.
# Averages are fairer because there are more weekdays than weekend days.
day_average = day.groupby("day_type")[["casual", "registered"]].mean()
day_average = day_average.reindex(["Weekday", "Weekend"])
print("\nAVERAGE RENTALS PER DAY")
print(day_average.round(1))
day_average.round(1).to_csv(results_folder / "weekday_weekend.csv")

day_average.plot(kind="bar", title="Average Daily Rentals: Weekday vs Weekend", rot=0)
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "02_weekday_weekend.png")
plt.close()

# 6. Find when customers rent bikes during the day.
# The hourly values below are averages per observed hourly record.
weekday_hours = hour[hour["day_type"] == "Weekday"].groupby("hr")[["casual", "registered"]].mean()
weekend_hours = hour[hour["day_type"] == "Weekend"].groupby("hr")[["casual", "registered"]].mean()

print("\nBUSIEST HOURS")
print(f"Weekday registered peak: {weekday_hours['registered'].idxmax()}:00")
print(f"Weekday casual peak: {weekday_hours['casual'].idxmax()}:00")
print(f"Weekend registered peak: {weekend_hours['registered'].idxmax()}:00")
print(f"Weekend casual peak: {weekend_hours['casual'].idxmax()}:00")
weekday_hours.round(1).to_csv(results_folder / "weekday_hourly.csv")
weekend_hours.round(1).to_csv(results_folder / "weekend_hourly.csv")

weekday_hours.plot(kind="line", marker="o", title="Weekday Rentals by Hour")
plt.xlabel("Hour (0-23)")
plt.ylabel("Average rentals per observed hour")
plt.tight_layout()
plt.savefig(charts_folder / "03_weekday_hours.png")
plt.close()

weekend_hours.plot(kind="line", marker="o", title="Weekend Rentals by Hour")
plt.xlabel("Hour (0-23)")
plt.ylabel("Average rentals per observed hour")
plt.tight_layout()
plt.savefig(charts_folder / "04_weekend_hours.png")
plt.close()

# 7. Compare seasonal demand, again using daily averages.
season_average = day.groupby("season_name")[["casual", "registered"]].mean()
season_average = season_average.reindex(["Spring", "Summer", "Fall", "Winter"])
print("\nAVERAGE RENTALS PER DAY BY SEASON")
print(season_average.round(1))
season_average.round(1).to_csv(results_folder / "seasons.csv")

season_average.plot(kind="bar", title="Average Daily Rentals by Season", rot=0)
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "05_seasons.png")
plt.close()

# 8. Compare demand across different weather conditions.
weather_average = day.groupby("weather_name")[["casual", "registered"]].mean()
print("\nAVERAGE RENTALS PER DAY BY WEATHER")
print(weather_average.round(1))
weather_average.round(1).to_csv(results_folder / "weather.csv")

weather_average.plot(kind="bar", title="Average Daily Rentals by Weather", rot=20)
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "06_weather.png")
plt.close()

print("\nDONE! Six charts were saved in:")
print(charts_folder)
print("The numerical tables were saved in:")
print(results_folder)
print("Note: These are rental transactions, not counts of unique customers.")

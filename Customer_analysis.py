# Bike-sharing demand analysis.
# Member 1, Ankit Kar: load the files, check them, and share the cleaned dataset.
# Member 2, Ahmad: hourly demand, weekdays, months, and seasons.
# Member 4, Tariq: casual and registered riders, and the chart labels.
# Member 5, Abhinav Singh: which factors matter, and the demand estimate.
# Member 3, Timothy: weather_analysis.py covers temperature, humidity, wind, and the correlation tests.

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
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
assert (day["casual"] + day["registered"] == day["cnt"]).all()

# 3. Add labels to make analysis easier.
# In this dataset, 0 = Sunday and 6 = Saturday.
day["day_type"] = "Weekday"
day.loc[day["weekday"].isin([0, 6]), "day_type"] = "Weekend"

hour["day_type"] = "Weekday"
hour.loc[hour["weekday"].isin([0, 6]), "day_type"] = "Weekend"

# The source dictionary calls 1 spring, 2 summer, 3 fall, and 4 winter.
# The dates do not match those names. Code 1 runs 21 Dec-20 Mar, code 2 runs
# 21 Mar-20 Jun, code 3 runs 21 Jun-22 Sep, and code 4 runs 23 Sep-20 Dec.
season_names = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
day["season_name"] = day["season"].map(season_names)
hour["season_name"] = hour["season"].map(season_names)

weather_names = {
    1: "Clear / partly cloudy",
    2: "Mist / cloudy",
    3: "Light rain / snow",
    4: "Severe weather",
}
weather_order = [
    "Clear / partly cloudy",
    "Mist / cloudy",
    "Light rain / snow",
]
day["weather_name"] = day["weathersit"].map(weather_names)
hour["weather_name"] = hour["weathersit"].map(weather_names)

weekday_names = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
}
weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
day["weekday_name"] = day["weekday"].map(weekday_names)
day["year_name"] = day["yr"].map({0: "2011", 1: "2012"})

# Holidays in this file all fall on Monday-Friday, so they sit inside the
# weekday bucket above. Keep that bucket, and also split the three schedules.
day["schedule"] = "Working day"
day.loc[day["weekday"].isin([0, 6]), "schedule"] = "Weekend"
day.loc[day["holiday"] == 1, "schedule"] = "Holiday"
schedule_order = ["Working day", "Weekend", "Holiday"]
hour["schedule"] = "Working day"
hour.loc[hour["weekday"].isin([0, 6]), "schedule"] = "Weekend"
hour.loc[hour["holiday"] == 1, "schedule"] = "Holiday"

month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}
day["month_name"] = day["mnth"].map(month_names)
hour["month_name"] = hour["mnth"].map(month_names)

# Member 1: write a cleaned copy the rest of the team can use.
# Original day.csv and hour.csv stay as downloaded.
# Humidity recorded as 0 is cleared, and the rental counts are kept.
hours_per_day = hour.groupby("dteday").size()
cleaned_day = day.copy()
cleaned_hour = hour.copy()
cleaned_day["temperature_c"] = cleaned_day["temp"] * 41
cleaned_hour["temperature_c"] = cleaned_hour["temp"] * 41
cleaned_day["humidity_pct"] = cleaned_day["hum"] * 100
cleaned_hour["humidity_pct"] = cleaned_hour["hum"] * 100
cleaned_day["wind_speed_kmh"] = cleaned_day["windspeed"] * 67
cleaned_hour["wind_speed_kmh"] = cleaned_hour["windspeed"] * 67
cleaned_day["zero_humidity_flag"] = (cleaned_day["hum"] == 0).astype(int)
cleaned_hour["zero_humidity_flag"] = (cleaned_hour["hum"] == 0).astype(int)
cleaned_day.loc[cleaned_day["zero_humidity_flag"] == 1, "humidity_pct"] = pd.NA
cleaned_hour.loc[cleaned_hour["zero_humidity_flag"] == 1, "humidity_pct"] = pd.NA
cleaned_day["hours_observed"] = cleaned_day["dteday"].map(hours_per_day)
cleaned_day["short_day_flag"] = (cleaned_day["hours_observed"] < 20).astype(int)
cleaned_hour["short_day_flag"] = cleaned_hour["dteday"].map(
    cleaned_day.set_index("dteday")["short_day_flag"]
)
cleaned_day["sandy_flag"] = (cleaned_day["dteday"] == "2012-10-29").astype(int)
cleaned_hour["sandy_flag"] = (cleaned_hour["dteday"] == "2012-10-29").astype(int)
cleaned_day["severe_weather_flag"] = (cleaned_day["weathersit"] == 4).astype(int)
cleaned_hour["severe_weather_flag"] = (cleaned_hour["weathersit"] == 4).astype(int)
cleaned_day.to_csv(data_folder / "day_cleaned.csv", index=False)
cleaned_hour.to_csv(data_folder / "hour_cleaned.csv", index=False)
assert int(cleaned_day["cnt"].sum()) == int(day["cnt"].sum())
print("\nCLEANED DATASET")
print(f"Saved {data_folder / 'day_cleaned.csv'} and {data_folder / 'hour_cleaned.csv'}")
print(f"Zero-humidity rows flagged: {int(cleaned_hour['zero_humidity_flag'].sum())} hours")

print("\nSEASON LABELS")
print("Source dictionary names do not match the calendar.")
print("Code 1 is labeled Winter here (21 Dec-20 Mar).")
print(pd.crosstab(day["season_name"], day["mnth"]).reindex(["Winter", "Spring", "Summer", "Fall"]))

# 4. Member 4, Tariq: compare casual and registered rentals.
totals = day[["casual", "registered"]].sum()
all_rentals = totals.sum()
print("\nCUSTOMER ANALYSIS: 2011-2012")
print("----------------------------")
print(f"Total rentals: {all_rentals:,}")
print(f"Casual: {totals['casual']:,} ({totals['casual'] / all_rentals:.1%})")
print(f"Registered: {totals['registered']:,} ({totals['registered'] / all_rentals:.1%})")
print("Note: These are rental transactions, not counts of unique customers.")
totals.to_csv(results_folder / "customer_totals.csv")

totals.plot(kind="bar", title="Total Rentals by Customer Type\nRegistered riders make up most of the rentals", rot=0)
plt.xlabel("Rider type")
plt.ylabel("Number of rentals")
plt.tight_layout()
plt.savefig(charts_folder / "01_customer_types.png")
plt.close()

# 5. Member 2, Ahmad, and Member 4, Tariq: weekdays and weekends.
# Averages are fairer because there are more weekdays than weekend days.
# This weekday average still includes 21 holidays.
day_average = day.groupby("day_type")[["casual", "registered"]].mean()
day_average = day_average.reindex(["Weekday", "Weekend"])
print("\nAVERAGE RENTALS PER DAY")
print(day_average.round(1))
print(f"Weekdays in this split include {(day['holiday'] == 1).sum()} holidays.")
day_average.round(1).to_csv(results_folder / "weekday_weekend.csv")

day_average.plot(
    kind="bar",
    title="Average Daily Rentals: Weekday vs Weekend\nDaily totals are close; the rider mix changes",
    rot=0,
)
plt.xlabel("")
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "02_weekday_weekend.png")
plt.close()

# 6. Member 2, Ahmad: hourly demand. The values are averages per observed hour.
# The hourly values below are averages per observed hourly record.
weekday_hours = hour[hour["day_type"] == "Weekday"].groupby("hr")[["casual", "registered"]].mean()
weekend_hours = hour[hour["day_type"] == "Weekend"].groupby("hr")[["casual", "registered"]].mean()
working_hours = hour[hour["workingday"] == 1].groupby("hr")[["casual", "registered"]].mean()

print("\nBUSIEST HOURS")
print(f"Weekday registered peak: {weekday_hours['registered'].idxmax()}:00")
print(f"Weekday casual peak: {weekday_hours['casual'].idxmax()}:00")
print(f"Weekend registered peak: {weekend_hours['registered'].idxmax()}:00")
print(f"Weekend casual peak: {weekend_hours['casual'].idxmax()}:00")
print(f"Working-day registered peak, holidays removed: {working_hours['registered'].idxmax()}:00")
print(f"Working-day casual peak, holidays removed: {working_hours['casual'].idxmax()}:00")
weekday_hours.round(1).to_csv(results_folder / "weekday_hourly.csv")
weekend_hours.round(1).to_csv(results_folder / "weekend_hourly.csv")
working_hours.round(1).to_csv(results_folder / "workingday_hourly.csv")

weekday_hours.plot(
    kind="line",
    marker="o",
    title="Weekday Rentals by Hour\nRegistered demand peaks at 08:00 and 17:00",
)
plt.xlabel("Hour (0-23)")
plt.ylabel("Average rentals per observed hour")
plt.tight_layout()
plt.savefig(charts_folder / "03_weekday_hours.png")
plt.close()

weekend_hours.plot(
    kind="line",
    marker="o",
    title="Weekend Rentals by Hour\nDemand peaks from late morning through mid-afternoon",
)
plt.xlabel("Hour (0-23)")
plt.ylabel("Average rentals per observed hour")
plt.tight_layout()
plt.savefig(charts_folder / "04_weekend_hours.png")
plt.close()

# 7. Member 2, Ahmad: seasonal demand, using calendar names and daily averages.
season_average = day.groupby("season_name")[["casual", "registered"]].mean()
season_average = season_average.reindex(["Winter", "Spring", "Summer", "Fall"])
print("\nAVERAGE RENTALS PER DAY BY SEASON")
print(season_average.round(1))
season_average.round(1).to_csv(results_folder / "seasons.csv")

season_average.plot(
    kind="bar",
    title="Average Daily Rentals by Season\nSummer is highest and winter is lowest",
    rot=0,
)
plt.xlabel("Season")
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "05_seasons.png")
plt.close()

# 8. Member 2, Ahmad: monthly demand, using the average per day.
month_average = day.groupby("month_name")[["casual", "registered", "cnt"]].mean()
month_average = month_average.reindex(list(month_names.values()))
print("\nAVERAGE RENTALS PER DAY BY MONTH")
print(month_average.round(1))
print(f"Highest month: {month_average['cnt'].idxmax()}")
print(f"Lowest month: {month_average['cnt'].idxmin()}")
month_average.round(1).to_csv(results_folder / "months.csv")

month_average[["casual", "registered"]].plot(
    kind="bar",
    title=(
        "Average Daily Rentals by Month\n"
        f"{month_average['cnt'].idxmax()} is highest and {month_average['cnt'].idxmin()} is lowest"
    ),
    rot=45,
)
plt.xlabel("Month")
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "17_month.png")
plt.close()

# 9. Record limits before reading the weather averages.
light_rain = day["weather_name"] == "Light rain / snow"
light_rain_with_sandy = float(day.loc[light_rain, "cnt"].mean())
light_rain_without_sandy = float(day.loc[light_rain & (day["dteday"] != "2012-10-29"), "cnt"].mean())
data_quality = pd.DataFrame(
    [
        {
            "check": "zero_humidity_day",
            "value": "2011-03-10",
            "note": f"{int((hour['hum'] == 0).sum())} hourly rows have humidity 0. Rentals stay in the demand totals. The day is excluded from the humidity correlation and from model fitting.",
        },
        {
            "check": "missing_hour_rows",
            "value": str(len(day) * 24 - len(hour)),
            "note": "Absent hour rows are mostly 03:00 and 04:00. Hourly charts are averages per observed hour.",
        },
        {
            "check": "short_days",
            "value": str(int((hours_per_day < 20).sum())),
            "note": "Days with fewer than 20 observed hours.",
        },
        {
            "check": "sandy_day",
            "value": "2012-10-29",
            "note": f"1 observed hour and {int(day.loc[day['dteday'] == '2012-10-29', 'cnt'].iloc[0])} rentals, coded light rain/snow.",
        },
        {
            "check": "light_rain_mean_with_sandy",
            "value": f"{light_rain_with_sandy:.1f}",
            "note": "Average daily rentals on light rain/snow days, including 29 Oct 2012.",
        },
        {
            "check": "light_rain_mean_without_sandy",
            "value": f"{light_rain_without_sandy:.1f}",
            "note": "Average daily rentals on the other light rain/snow days.",
        },
        {
            "check": "severe_weather_hours",
            "value": str(int((hour["weathersit"] == 4).sum())),
            "note": "Too few hours to draw an hourly severe-weather pattern. Omitted from the hourly weather chart.",
        },
        {
            "check": "severe_weather_days",
            "value": str(int((day["weathersit"] == 4).sum())),
            "note": "No day is coded severe weather, so the daily weather chart has three bars.",
        },
        {
            "check": "season_names",
            "value": "calendar",
            "note": "Source dictionary labels are reversed relative to the dates. Charts use Winter, Spring, Summer, and Fall.",
        },
    ]
)
print("\nDATA LIMITS")
print(data_quality.to_string(index=False))
data_quality.to_csv(results_folder / "data_quality.csv", index=False)

# 10. Member 4, Tariq: weather split by rider type. Daily data has no severe-weather days.
# Daily data has no severe-weather days. Keep the three conditions that occur,
# in weather order rather than alphabetical order.
weather_average = day.groupby("weather_name")[["casual", "registered"]].mean()
weather_average = weather_average.reindex(weather_order)
print("\nAVERAGE RENTALS PER DAY BY WEATHER")
print(weather_average.round(1))
print("Severe weather has", int((day["weathersit"] == 4).sum()), "daily rows and", int((hour["weathersit"] == 4).sum()), "hourly rows.")
weather_average.round(1).to_csv(results_folder / "weather.csv")

weather_average.plot(
    kind="bar",
    title="Average Daily Rentals by Weather\nLight rain or snow cuts casual and registered rentals",
    rot=15,
)
plt.xlabel("Weather")
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "06_weather.png")
plt.close()

# 11. Member 2, Ahmad: which day of the week has the highest demand?
dow_average = day.groupby("weekday_name")[["casual", "registered", "cnt"]].mean()
dow_average = dow_average.reindex(weekday_order)
print("\nAVERAGE RENTALS PER DAY BY WEEKDAY")
print(dow_average.round(1))
print(f"Highest total: {dow_average['cnt'].idxmax()}")
print(f"Lowest total: {dow_average['cnt'].idxmin()}")
dow_average.round(1).to_csv(results_folder / "day_of_week.csv")

dow_average[["casual", "registered"]].plot(
    kind="bar",
    title="Average Daily Rentals by Day of Week\nFriday is highest and Sunday is lowest",
    rot=30,
)
plt.xlabel("Day of week")
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "07_day_of_week.png")
plt.close()

# 12. Member 2, Ahmad: working days, weekends, and holidays.
schedule_average = day.groupby("schedule")[["casual", "registered", "cnt"]].mean()
schedule_average = schedule_average.reindex(schedule_order)
schedule_counts = day["schedule"].value_counts().reindex(schedule_order)
print("\nAVERAGE RENTALS BY SCHEDULE")
print(pd.concat([schedule_counts.rename("days"), schedule_average.round(1)], axis=1))
schedule_average.round(1).to_csv(results_folder / "schedule.csv")

schedule_average[["casual", "registered"]].plot(
    kind="bar",
    title="Average Daily Rentals: Working Day, Weekend, Holiday\nHolidays are quieter and have a larger casual share",
    rot=0,
)
plt.xlabel("Schedule")
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "08_schedule.png")
plt.close()

# 13. Member 2, Ahmad: demand grew from 2011 to 2012. Pooled averages hide that.
year_average = day.groupby("year_name")[["casual", "registered", "cnt"]].mean()
year_average = year_average.reindex(["2011", "2012"])
print("\nAVERAGE RENTALS PER DAY BY YEAR")
print(year_average.round(1))
year_average.round(1).to_csv(results_folder / "year.csv")

year_average[["casual", "registered"]].plot(
    kind="bar",
    title="Average Daily Rentals by Year\n2012 is much higher than 2011",
    rot=0,
)
plt.xlabel("Year")
plt.ylabel("Average rentals per day")
plt.tight_layout()
plt.savefig(charts_folder / "09_year.png")
plt.close()

# 14. Member 5, Abhinav Singh: which factors move demand the most?
# Eta-squared is the share of variation captured by differences in group averages.
# Temperature uses r-squared so it can sit on the same scale. Customer type is
# reported as a change in mix, because it splits rentals rather than creating them.


def eta_squared(frame: pd.DataFrame, group_col: str, value_col: str) -> float:
    values = frame[value_col]
    overall = values.mean()
    ss_total = ((values - overall) ** 2).sum()
    group_means = frame.groupby(group_col)[value_col].transform("mean")
    ss_between = ((group_means - overall) ** 2).sum()
    return float(ss_between / ss_total)


def factor_row(
    frame: pd.DataFrame,
    group_col: str,
    value_col: str,
    factor: str,
    scope: str,
) -> dict[str, object]:
    means = frame.groupby(group_col)[value_col].mean()
    low_name = str(means.idxmin())
    high_name = str(means.idxmax())
    return {
        "factor": factor,
        "scope": scope,
        "share_of_variation": round(eta_squared(frame, group_col, value_col), 3),
        "low_group": low_name,
        "high_group": high_name,
        "low_mean": round(float(means.min()), 1),
        "high_mean": round(float(means.max()), 1),
        "mean_gap": round(float(means.max() - means.min()), 1),
    }


humidity_ok = day["hum"] > 0
temperature = day.loc[humidity_ok, "temp"] * 41
rentals_for_temp = day.loc[humidity_ok, "cnt"]
temp_r = float(temperature.corr(rentals_for_temp))
hour_for_weather = hour[hour["weathersit"] < 4]
factor_rows = [
    factor_row(day, "year_name", "cnt", "Year", "Daily rentals"),
    factor_row(day, "season_name", "cnt", "Season", "Daily rentals"),
    factor_row(day, "weather_name", "cnt", "Weather situation", "Daily rentals"),
    factor_row(day, "weekday_name", "cnt", "Day of week", "Daily rentals"),
    factor_row(day, "schedule", "cnt", "Working day / weekend / holiday", "Daily rentals"),
    factor_row(hour, "hr", "cnt", "Hour of day", "Hourly rentals"),
    factor_row(hour_for_weather, "weather_name", "cnt", "Weather situation", "Hourly rentals"),
    {
        "factor": "Temperature (r-squared)",
        "scope": "Daily rentals",
        "share_of_variation": round(temp_r ** 2, 3),
        "low_group": "Colder days",
        "high_group": "Warmer days",
        "low_mean": None,
        "high_mean": None,
        "mean_gap": None,
    },
]
weekday_casual_share = day.loc[day["day_type"] == "Weekday", "casual"].sum() / day.loc[day["day_type"] == "Weekday", "cnt"].sum()
weekend_casual_share = day.loc[day["day_type"] == "Weekend", "casual"].sum() / day.loc[day["day_type"] == "Weekend", "cnt"].sum()
factor_rows.append(
    {
        "factor": "Customer type",
        "scope": "Share of daily rentals",
        "share_of_variation": None,
        "low_group": "Weekday casual share",
        "high_group": "Weekend casual share",
        "low_mean": round(float(weekday_casual_share), 3),
        "high_mean": round(float(weekend_casual_share), 3),
        "mean_gap": round(float(weekend_casual_share - weekday_casual_share), 3),
    }
)
factors = pd.DataFrame(factor_rows)
print("\nFACTOR INFLUENCE")
print(factors.to_string(index=False))
factors.to_csv(results_folder / "factor_influence.csv", index=False)

daily_factors = factors[factors["scope"] == "Daily rentals"].sort_values("share_of_variation")
daily_factors.plot(
    kind="barh",
    x="factor",
    y="share_of_variation",
    legend=False,
    title="Share of Daily Rental Variation",
)
plt.xlabel("Share of variation")
plt.ylabel("Factor")
plt.tight_layout()
plt.savefig(charts_folder / "10_factor_influence.png")
plt.close()

# 15. Member 5, Abhinav Singh: can historical data estimate later demand?
# Train on days before 1 Oct 2012 and test on the rest of 2012.
# The calendar-only model is the planning figure, because it does not use that day's weather.
# The known-weather model uses the test day's temperature, humidity, wind, and weather.
# Those values are not available when the plan is made, so its error is smaller than a real forecast.
# The 2011-03-10 humidity value is 0, so that day is left out of fitting only.
train_end = "2012-10-01"
model_day = day.loc[day["hum"] > 0].copy()
train = model_day[model_day["dteday"] < train_end]
test = day[day["dteday"] >= train_end].copy()


def model_matrix(frame: pd.DataFrame, include_year: bool, include_weather: bool) -> pd.DataFrame:
    matrix = pd.DataFrame(
        {
            "intercept": 1.0,
            "holiday": frame["holiday"].astype(float),
            "workingday": frame["workingday"].astype(float),
        },
        index=frame.index,
    )
    if include_weather:
        matrix["temp"] = frame["temp"].astype(float)
        matrix["hum"] = frame["hum"].astype(float)
        matrix["windspeed"] = frame["windspeed"].astype(float)
    if include_year:
        matrix["year_2012"] = (frame["yr"] == 1).astype(float)
    for season_label in ["Spring", "Summer", "Fall"]:
        matrix[f"season_{season_label}"] = (frame["season_name"] == season_label).astype(float)
    if include_weather:
        for weather_label in ["Mist / cloudy", "Light rain / snow"]:
            safe_label = weather_label.split()[0]
            matrix[f"weather_{safe_label}"] = (frame["weather_name"] == weather_label).astype(float)
    return matrix


def fit_predict(include_year: bool, include_weather: bool) -> tuple[pd.Series, pd.Series]:
    x_train = model_matrix(train, include_year, include_weather)
    y_train = train["cnt"].astype(float)
    x_test = model_matrix(test, include_year, include_weather)
    coefficients, _, _, _ = np.linalg.lstsq(
        x_train.to_numpy(dtype=float),
        y_train.to_numpy(dtype=float),
        rcond=None,
    )
    predicted = pd.Series(
        np.dot(x_test.to_numpy(dtype=float), coefficients),
        index=test.index,
        name="predicted",
    )
    named = pd.Series(coefficients, index=x_train.columns, name="coefficient")
    return predicted, named


def error_row(name: str, actual: pd.Series, predicted: pd.Series) -> dict[str, object]:
    error = actual - predicted
    return {
        "model": name,
        "test_days": int(len(actual)),
        "mae": round(float(error.abs().mean()), 1),
        "rmse": round(float((error ** 2).mean() ** 0.5), 1),
        "mean_actual": round(float(actual.mean()), 1),
        "mean_predicted": round(float(predicted.mean()), 1),
    }


predicted_with_year, coefficients_with_year = fit_predict(True, True)
predicted_without_year, _ = fit_predict(False, True)
predicted_calendar, _ = fit_predict(True, False)
training_mean = pd.Series(float(train["cnt"].mean()), index=test.index)
previous_year_dates = (pd.to_datetime(test["dteday"]) - pd.DateOffset(years=1)).dt.strftime("%Y-%m-%d")
previous_year = day.set_index("dteday").loc[previous_year_dates, "cnt"].astype(float)
previous_year.index = test.index

actual_test = test["cnt"].astype(float)
sandy_mask = test["dteday"] != "2012-10-29"
metrics = pd.DataFrame(
    [
        error_row("Training average", actual_test, training_mean),
        error_row("Same date in 2011", actual_test, previous_year),
        error_row("Calendar only, with year", actual_test, predicted_calendar),
        error_row("Known weather, without year", actual_test, predicted_without_year),
        error_row("Known weather, with year", actual_test, predicted_with_year),
        error_row(
            "Known weather, with year, excluding 29 Oct 2012",
            actual_test[sandy_mask],
            predicted_with_year[sandy_mask],
        ),
    ]
)
print("\nDEMAND ESTIMATE: 1 OCT 2012 TO 31 DEC 2012")
print(metrics.to_string(index=False))
metrics.to_csv(results_folder / "forecast_metrics.csv", index=False)
coefficients_with_year.round(1).to_csv(results_folder / "forecast_coefficients.csv")

forecast_plot = pd.DataFrame(
    {
        "Actual": actual_test.to_numpy(),
        "Calendar only": predicted_calendar.to_numpy(),
        "Known weather": predicted_with_year.to_numpy(),
    },
    index=pd.to_datetime(test["dteday"]),
)
axis = forecast_plot.plot(
    title="Holdout Demand Estimate, Last Quarter of 2012\nCalendar only is the figure available before the day",
)
axis.set_xlabel("")
axis.set_ylabel("Daily rentals")
axis.get_figure().set_size_inches(10, 4)
plt.tight_layout()
plt.savefig(charts_folder / "11_forecast.png")
plt.close()

print("\nDONE")
print(charts_folder)
print(results_folder)

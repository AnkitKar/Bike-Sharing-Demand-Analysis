# Data dictionary

Capital Bikeshare, Washington, D.C. The original files are `data/day.csv` (731 days, 1 January 2011 to 31 December 2012) and `data/hour.csv` (17,379 hours). `data/day_cleaned.csv` and `data/hour_cleaned.csv` keep every rental row and add the columns below.

The source file says temperature is divided by 41, feeling temperature by 50, humidity by 100, and wind speed by 67.

## Columns in the original files

| Column | Meaning |
| --- | --- |
| instant | Row number. |
| dteday | Date, YYYY-MM-DD. |
| season | Season code. The source dictionary says 1 spring, 2 summer, 3 fall, 4 winter. The dates run the other way: 1 is 21 Dec-20 Mar, 2 is 21 Mar-20 Jun, 3 is 21 Jun-22 Sep, 4 is 23 Sep-20 Dec. |
| yr | 0 is 2011. 1 is 2012. |
| mnth | Month number, 1 to 12. |
| hr | Hour, 0 to 23. Present in `hour.csv` only. |
| holiday | 1 if the date is a holiday, otherwise 0. |
| weekday | Day of week. 0 is Sunday and 6 is Saturday. Checked against `dteday`. |
| workingday | 1 if the day is neither a weekend nor a holiday. |
| weathersit | 1 clear or partly cloudy. 2 mist or cloudy. 3 light rain or snow. 4 severe weather. Code 4 occurs in 3 hours and on 0 days. |
| temp | Temperature divided by 41. Multiply by 41 for Celsius. |
| atemp | Feeling temperature divided by 50. |
| hum | Humidity divided by 100. A value of 0 on 10 March 2011 is a bad reading. |
| windspeed | Wind speed divided by 67. Multiply by 67 for km/h. |
| casual | Rentals by casual riders. These are transactions, not unique people. |
| registered | Rentals by registered riders. |
| cnt | casual plus registered. |

## Columns added in the cleaned files

| Column | Meaning |
| --- | --- |
| day_type | Weekday or Weekend. Weekend is Sunday and Saturday. Holidays that fall on Monday-Friday stay in Weekday. |
| season_name | Calendar name: Winter, Spring, Summer, Fall. See the season note above. |
| weather_name | Clear / partly cloudy, Mist / cloudy, Light rain / snow, or Severe weather. |
| weekday_name | Sunday through Saturday. On the daily cleaned file. |
| year_name | 2011 or 2012. On the daily cleaned file. |
| schedule | Working day, Weekend, or Holiday. Holiday wins when a date is both a weekday and a holiday. |
| month_name | January through December. |
| temperature_c | temp times 41. |
| humidity_pct | hum times 100. Blank where the source humidity is 0. |
| wind_speed_kmh | windspeed times 67. |
| zero_humidity_flag | 1 when the source humidity is 0. |
| hours_observed | How many hour rows exist for that date. Daily file only. A full day has 24. |
| short_day_flag | 1 when the date has fewer than 20 observed hours. |
| sandy_flag | 1 on 29 October 2012. |
| severe_weather_flag | 1 when weathersit is 4. |

## Checks

Daily and hourly `cnt` both sum to 3,292,679. Casual plus registered equals `cnt` on every daily row. There are no blank cells in the original files and no missing calendar dates. 165 hour rows are absent, mostly at 03:00 and 04:00. The cleaned files do not invent those hours.

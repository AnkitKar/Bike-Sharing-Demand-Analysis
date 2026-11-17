# Bike-Sharing Demand Analysis

Technical report. Capital Bikeshare, Washington, D.C., daily and hourly rentals for 2011 and 2012.

## Objective

The company needs to place bicycles where people will rent them. Demand changes by hour, day, season, weather, and rider type. This analysis uses the historical rental file to describe those patterns, rank the factors that move demand, and turn the results into operational actions.

The questions are:

- At what hours is rental demand highest?
- Which days of the week have the highest demand?
- How do seasons influence rentals?
- How do weather conditions affect demand?
- How do casual and registered riders differ?
- Can historical data estimate later demand?

## Data and checks

The file has 731 days, from 1 January 2011 through 31 December 2012, and 17,379 hour rows. Daily rentals and hourly rentals both sum to 3,292,679. Casual plus registered equals the total on every day. There are no blank cells, no duplicate dates, and no missing calendar days. `data/day_cleaned.csv` and `data/hour_cleaned.csv` keep those rental counts, add the labels in `DATA_DICTIONARY.md`, and clear humidity where the source value is 0.

Four limits sit in front of the weather results. They are saved in `results/data_quality.csv`.

- On 10 March 2011, humidity is recorded as 0 for 22 hours. The rental counts on that day are kept in the demand totals. The day is left out of the humidity chart, the humidity correlation, and the model fit.
- 165 hour rows are absent, mostly at 03:00 and 04:00. Eight days have fewer than 20 observed hours. Hourly charts are averages per observed hour.
- 29 October 2012, during Hurricane Sandy, has one observed hour and 22 rentals. The day is coded light rain/snow, so it pulls that weather average down. The light-rain average is 1,803 with that day and 1,892 without it.
- Weather code 4, severe weather, occurs in three hours and on zero days: 26 January 2011 at 16:00 (36 rentals), 9 January 2012 at 18:00 (164), and 21 January 2012 at 01:00 (23). Those three hours are listed and are omitted from the hourly weather chart.

The source dictionary labels season codes as spring, summer, fall, and winter. The dates run the other way. Code 1 is 21 December–20 March, code 2 is 21 March–20 June, code 3 is 21 June–22 September, and code 4 is 23 September–20 December. This report uses the calendar names Winter, Spring, Summer, and Fall. The month counts behind that choice are in the customer-analysis output.

In this file, weekday 0 is Sunday and weekday 6 is Saturday. That coding was checked against the dates.

## Method

Daily comparisons use the average per day, so a group with more days does not look larger only because it contains more days. Hourly comparisons use the average per observed hour.

Influence is measured in two ways. For groups such as season and weather, eta-squared is the share of rental variation that sits between the group averages. For temperature, the comparable figure is r-squared, the linear association. Customer type is reported as a change in mix, because casual and registered counts split the same rentals.

Weather correlations are Pearson correlations. Each one is tested against a zero association, and the p-values are in `results/weather_correlations.csv`. Temperature, humidity, and wind speed are all below 0.05 in this file. Humidity remains the weak association: r = −0.101 on all days, and r = −0.115 after the zero-humidity day is removed, which is −0.11 at two decimals.

The demand estimate is an ordinary least-squares model of daily rentals. The fit uses days before 1 October 2012, excluding the zero-humidity day. The test is 1 October 2012 through 31 December 2012 (92 days). The planning model uses year, season, holiday, and working day. It does not use that day's weather. A second model adds the test day's temperature, humidity, wind, and weather situation. That second error is smaller because those values are already known, so it is not the error of a plan made in advance. Comparison estimates are the training-period average and the same calendar date in 2011. The coefficients are not used to rank factors, because season and temperature describe overlapping parts of the same pattern. The ranking is the separate share-of-variation table.

## Findings

1. Registered riders account for 2,672,662 rentals (81.2 percent) and casual riders for 620,017 (18.8 percent). On weekdays the casual share is 13.7 percent. On weekends it is 31.9 percent. Registered demand on weekdays peaks at 08:00 (442 rentals in the average hour) and 17:00 (458). Weekend registered demand peaks at 12:00 and weekend casual demand peaks at 14:00. Taking the 21 holidays out of the working-day hours leaves the peaks at 17:00.

2. Friday has the highest daily average (4,690) and Sunday the lowest (4,229). Day of week explains 0.6 percent of daily variation. The weekday average (4,551) and the weekend average (4,390) are close. The useful day-of-week difference is who is riding, and at what hour. Holidays are the exception: 21 holidays average 3,735 rentals, against 4,585 on working days. Those holidays fall on Monday–Friday, so a weekday average that does not separate them mixes a commute day with a holiday.

3. Summer averages 5,644 rentals a day and winter averages 2,604. Spring averages 4,992 and fall averages 4,728. Season accounts for 34.7 percent of daily variation. By month, June is highest at 5,772 and January is lowest at 2,176. September is close to June at 5,767. Summer is the season to staff and stock at the high end. Winter is the season to run a smaller fleet. A chart that follows the source dictionary would attach the winter low to the name “spring” and the summer high to the name “fall.”

4. Clear or partly cloudy days average 4,877 rentals, mist or cloudy days 4,036, and light rain or snow 1,803. Light rain is about 37 percent of a clear day. Casual rentals fall especially hard in that weather, from 964 on clear days to 185. The 17:00 peak remains under clear, mist, and light rain. Temperature has the strongest linear weather association (r = 0.627 on all days, r = 0.628 after dropping the zero-humidity day, r-squared = 0.394). Wind speed is weakly negative (r = −0.235). Humidity is weaker still (r = −0.101, or −0.115 after the zero-humidity day is removed). Severe weather does not have a usable hourly curve.

5. Average daily demand rose from 3,406 in 2011 to 5,600 in 2012, a 64 percent increase. Year accounts for 32.1 percent of daily variation. A fleet size taken from the two-year average sits below the 2012 level.

6. The factors do not all move demand in the same way. Hour of day accounts for 50.1 percent of hourly variation, from 6 rentals at 04:00 to 462 at 17:00. Across days, temperature (39.4 percent), season (34.7 percent), and year (32.1 percent) are the large shares. Weather situation has a large gap on the days it changes, about 3,074 rentals between clear and light rain, and still explains 9.9 percent of daily variation because only 21 days are coded light rain or snow. Day of week and the working-day/weekend/holiday split each explain under 1 percent of the daily total. Customer type changes the mix of riders. It does not, by itself, create a large gap in the daily total.

7. Historical daily data can estimate later demand when the year is included. On the last 92 days of 2012, the actual mean is 5,165. The calendar-only model, which uses year, season, holiday, and working day, has a mean absolute error of 1,358 and predicts 5,903. That is the planning figure. The training average is off by 1,752 and the same date in 2011 by 1,982. Adding that day's temperature, humidity, wind, and weather lowers the error to 885 and the prediction to 5,564. Those weather values are not known when the plan is made, so 885 is the known-weather error, not the advance forecast. Dropping 29 October 2012 lowers the known-weather error from 885 to 853. The same known-weather model without year predicts 3,678. This is a system-wide daily estimate. The file has no station locations, so it cannot assign bicycles to docks.

## Recommendations

1. Rebalance the fleet around the two working-day registered peaks. Move bicycles into commute positions before 08:00 and again before 17:00. On weekends, stage bicycles for late morning through mid-afternoon, when casual demand peaks around 14:00 and registered demand peaks around 12:00. The weekend job is a leisure pattern, and the working-day job is a commute pattern.

2. Set the seasonal fleet from the calendar, with the largest available fleet in summer (about 5,600 rentals a day in this history) and the smallest in winter (about 2,600). Spring and fall sit in between, near 5,000 and 4,700. Use Winter, Spring, Summer, and Fall as defined by the dates above. The season names in the source dictionary run in the opposite order.

3. Plan the day from the weather forecast and from temperature. A light-rain or light-snow day in this history averages about 1,800 rentals, against about 4,900 on a clear day, and the 17:00 peak still needs coverage. Humidity is a weak signal for staffing. A named storm is a separate case: 29 October 2012 produced 22 rentals, far below the ordinary light-rain day. Severe weather in the file is three hours, which is too little to write a standing hourly rule.

4. Set the base fleet from the 2012 level, about 5,600 rentals a day, and review it as demand grows. The 2011–2012 average understates the later year. Staff the 21 holidays nearer their own average of 3,735, with a larger casual share, rather than as a normal working day.

## What the project can now show

The cleaned patterns, charts, and tables are in `Customer_analysis.py`, `weather_analysis.py`, `charts/`, and `results/`. The notebook `bike_sharing_demand_analysis.ipynb` reruns both scripts. The team deck is `Bike Sharing Demand Analysis.pptx`.

The original questions are answered as follows.

- Hours: 08:00 and 17:00 on working days; midday on weekends.
- Days: Friday is highest and Sunday is lowest, by a small margin. The operational split is working day, weekend, and holiday.
- Seasons: summer is the high season and winter is the low season, using calendar names.
- Months: June is highest and January is lowest.
- Weather: clear days are highest, light rain or snow cuts demand to about 37 percent of a clear day, and temperature is the strong continuous signal.
- Customer type: registered riders dominate the commute; casual riders rise on weekends and fall sharply in bad weather.
- Estimation: the calendar-only model estimates the last quarter of 2012 with a mean absolute error of 1,358 rentals. Using that day's actual weather lowers the error to 885, and that weather is not available in advance.

The associations describe this two-year history. They are a basis for planning tests, and they are not proof that changing one condition will cause the average to move by the same amount.

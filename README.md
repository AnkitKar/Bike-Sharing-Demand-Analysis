# Bike-Sharing-Demand-Analysis

Capital Bikeshare rentals for 2011 and 2012. The question is how to place bicycles where demand actually is.

## Team

| Member | Name | Role |
| --- | --- | --- |
| 1 | Ankit Kar | Data Analyst. Dataset, cleaning, repository, and this dictionary. |
| 2 | Ahmad | Demand Analyst. Hours, days, months, and seasons. |
| 3 | Timothy | Weather Analyst. Temperature, humidity, wind, and correlation tests. |
| 4 | Tariq | Customer Analyst. Casual and registered riders, and the slides. |
| 5 | Abhinav Singh | Project lead. Demand estimate, findings, notebook, report, and deck. |

## How to run

From this folder, with pandas, matplotlib, numpy, and scipy installed:

```bash
python Customer_analysis.py
python weather_analysis.py
```

`bike_sharing_demand_analysis.ipynb` runs both scripts and shows the charts.

## Files

- `data/day.csv` and `data/hour.csv` are the original download.
- `data/day_cleaned.csv` and `data/hour_cleaned.csv` are the shared cleaned copies. Rental counts are unchanged. Labels are added, and humidity recorded as 0 is cleared.
- `DATA_DICTIONARY.md` defines every column.
- `charts/` and `results/` are the saved figures and tables.
- `technical_report.md` is the write-up.
- `Bike Sharing Demand Analysis.pptx` is the team deck.
- `Weather Analysis Slides.pptx` is Timothy's earlier weather deck and stays in the folder.

## Project agenda
How can a bike-sharing company optimize bicycle availability and resource allocation by understanding customer demand patterns and the factors influencing rentals?

A. Research Questions

Main Question – Strategic
How can a bike-sharing company optimize bicycle availability and resource allocation by understanding customer demand patterns and the factors influencing rentals?

Supporting Question 1 – Descriptive
What are the bike rental demand patterns across different hours, days, seasons and weather conditions?

Supporting Question 2 – Diagnostic
Which factors, such as time, weather, season and customer type, have the greatest influence on bike rental demand, and why?

Supporting Question 3 – Recommendation-oriented
What operational strategies can the bike-sharing company implement to improve bicycle availability, maximize fleet utilization and meet customer demand?

B. Business problem statement

Bike-sharing companies face challenges in efficiently managing bicycle availability due to fluctuating customer demand. Demand varies throughout the day and is influenced by weather conditions, seasons, holidays and working days. Without understanding these patterns, companies risk bicycle shortages during peak periods and underutilization during low-demand periods. This project aims to analyze historical bike rental data to identify demand patterns and provide data-driven recommendations for improving fleet utilization and operational efficiency.

Main objective

To identify the factors influencing bike-sharing demand and develop data-driven recommendations that help a bike-sharing company optimize bicycle availability and resource allocation.

Detailed Research questions

At what hours is bike rental demand highest? (Fleet allocation)
Which days of the week have the highest demand? (Operational planning)
How do seasons influence bike rentals? (Seasonal planning)
How do weather conditions affect rental demand? (Demand management)
How does customer behavior differ between casual and registered users? (Customer strategy)
Can we estimate bike rental demand using historical data? (Demand forecasting)

C. Success Criteria – How will we know our project was successful?

Our project will be successful if we can:

1. Analyze the data: Successfully clean and analyze the bike-sharing dataset.
2. Identify patterns: Understand peak rental hours, busy days, seasonal trends and weather impacts.
3. Generate insights: Identify at least 5 important findings from the analysis.
4. Make recommendations: Suggest at least 3 practical ways to improve bike availability and fleet utilization.
5. Complete the analysis: Create meaningful visualizations and perform statistical analysis.
6. Deliver the project: Successfully submit the Python notebook, technical report and team presentation.

Overall success: Turn historical bike rental data into useful insights and practical recommendations that help improve bike-sharing operations.

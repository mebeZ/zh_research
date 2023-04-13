# zh_research

Progress Notes (10/13):
- What was accomplished: 
  - Explored the different weather data links provided in the Weather Project Description
  - Set up an API key with Weather Underground service
  - Used the Python Request module plus API documentation to query the Weather Underground API for weather data from the past day for a specific location
  - Filter the incoming JSON data for specific attributes such as 'precipRate'
  - Wrote results in 5 minute intervals to a CSV format
  - "rainfall_04_10_2023" gives rainfall measurements at 5 minute intervals for the date of 4/10. 
- Next steps:
  - Aggregate data from mulitiple days (i.e. from January 2022 - June 2022) into the CSV file, while keeping measurements of 5 meters
    - Comment: The API only gives me finer measurements for the current day - I need to figure out how to get finer measurements for any date, either by         using the current API or finding a new one.
  - Use the "Location Services - Search" endpoint to find all weather stations in NYC and collect data for all of them 

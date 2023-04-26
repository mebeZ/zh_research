# zh_research

Progress Notes (10/26):
- What was accomplished:
  - Sought to get a list of personal weather stations located in New York City
  - I researched the WUnderground API. While the specification of Location Services - Search API indicates that it  should be able to retrieve all Personal Weather Stations in a particular city, I found that this was not the case     and that it retrieved extremely few results, many of which were not in New York City. 
  - However, the Location Services - Near API gave a list of the 10 nearest Personal Weather Stations from a given geocode (passed in as a parameter). I reasoned that I could iterate over the latitude/longitude ranges that bounded NYC, and for each geocode, make an API call to find the nearest stations, and add them to the set of PWS in NYC.
  - I found that New York City was bounded by latitude range: (40.50, 41.00) and longitude range (-73.7, -74.3). I iterated through lat/lon in increments of 0.05 and managed to extract a couple hundred of results. 
  - The problem is that not all of these results were in NYC (some were in New Jersey for example). I realized that I code use the 'geopy' library to 'reverse geocode': that is, given a geocode, find out which city it is located in. Thus, I would filter out the geocodes that were not located in NYC.
  - I realized that I could apply an even simpler approach. PWS's located in NYC all had names which started with 'KNYNEWYO.' Thus, I simply filtered for PWS's starting with this name.
  - I also designed a helper utility which takes as input a set of geocodes and draws a boundary of these geocodes. This helped me to see whether certain PWS's were actually in NYC and to check the latitude and longitude bounds of NYC.

- Next steps:
  - The script does not work for some Personal Weather Stations. This is very likely due to the fact that some of the PWS have data entries with NaN values and I call dropna() in one of my methods, which will drop all rows if there is at least one NULL entry. This should be a pretty trivial fix, I just have not gotten around to it. 
  - Data collection happens slowly. It takes 2 minutes to collect data from one PWS for a month. Thus, if we want to collect data for 50 PWS for a year, it would take 1200 minutes which is 20 hours. This is less than ideal, so I aim to make my methods more efficient in terms of runtime.
  - There seems to be a limit to the number of calls I can make to the WUnderground API in a set period of time. This may or may not be an issue (as I don't think I'll need to make that many calls), but I will research whether we can get upgraded API access.
  - I want to get the geocode coordinates of each active link on WimNet and then invoke the WUnderground Location Services - Near API on that geocode. This will allow us to find the nearest PWS to each active link.

Progress Notes (10/19):
- What was accomplished:
  - Asked online whether the Weather Underground API could give 5 minute intervals for an arbitrary date. Found out that this functionality was not enabled.
  - Decided to web scrape table data from Weather Underground site instead (specifically, a URL like this: https://www.wunderground.com/dashboard/pws/KNYNEWYO1238/table/2023-04-26/2023-04-26/daily)
  - Processed this data into a Pandas DataFrame, extracted the relevant features, and created a Datetime stamp for each entry
  - Wrote a script which lets the user specify a start and end date. It then iterates over each date, constructs the proper URL, and makes a get request. Finally it merges consecutive dataframes along Axis 0 in order to produce one single dataframe for the entire period. 
  - Write the dataframe to a CSV in the data/wunderground directory
  
- Next steps:
  - Extract a list of all Personal Weather Stations (PWS) located in New York City that are registered with the Weather Underground API
  - Run the script on each PWS and save the data as a CSV 

===========================================================

Progress Notes (10/12):
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

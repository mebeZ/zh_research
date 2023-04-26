"eGTFVYajGnbIFvqMFGbmAaumTWEZvnGU"

import requests
from datetime import datetime, timedelta

# Define the start and end dates
start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 6, 30)

# Define the time interval
interval = timedelta(minutes=5)

# Define the list of weather stations in New York City
url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt'
response = requests.get(url)
stations = []
for line in response.iter_lines():
    line = line.decode('utf-8')
    if line[0:2] == 'US' and line[38:44] == '+40.78' and line[45:51] == '-073.9':
        stations.append(line[0:11])

# Define the NOAA API endpoint and parameters
base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
params = {
    'datasetid': 'GHCND',
    'startdate': start_date.date().isoformat(),
    'enddate': end_date.date().isoformat(),
    'stationid': '',
    'units': 'metric',
    'datatypeid': 'PRCP',
    'limit': 1000,
    'offset': 0
}

# Loop through each weather station and retrieve the rain measurements
for station in stations:
    params['stationid'] = station
    while True:
        response = requests.get(base_url, params=params, headers={'token': 'YOUR_NOAA_TOKEN'})
        data = response.json()['results']
        if not data:
            break
        for result in data:
            date = datetime.strptime(result['date'], '%Y-%m-%dT%H:%M:%S')
            if date.minute % 5 == 0:
                print(station, date.isoformat(), result['value'])
        params['offset'] += params['limit']

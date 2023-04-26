import requests
import numpy as np
from geopy.geocoders import Nominatim

"""
pws-locator should return a list of all Personal Weather Stations (PWS) in a given city (i.e. New York City)
"""

# https://api.weather.com/v3/location/search?query=atlanta&locationType=locid&language=en-US&format=json&apiKey=yourApiKey 

class PWSLocator(object):

    def __init__(self):
        # Define the query parameters for the Near V3 API
        self.query_params = {'product':'pws', 'format':'json', 'apiKey':'329d28aca92149f19d28aca92139f1ea'}

        # Define the base URL for the Near V3 API
        self.base_url = 'https://api.weather.com/v3/location/near'

        # Initialize a set to store the unique PWS station IDs
        self.pws_set = set()

    def get_pws(self, lat_range=np.arange(40.590, 40.739, 0.05), lon_range=np.arange(-73.892, -74.033, -0.05)):

        # Iterate over the latitude and longitude ranges
        for lat in lat_range:
            for lon in lon_range:
                # Construct the geocode parameter
                geocode = '{:.4f},{:.4f}'.format(lat, lon)
                #print("geocode = ", geocode)

                """
                Reverse geocoding: Given (lat, lon), figure out the location
                ============================
                geolocator = Nominatim(user_agent="my_app_name")
                location = geolocator.reverse(lat, lon)
                city = location.raw['address']['city']
                if (city == "NYC" or city == "New York City"):
                    # Make the API request
                """

                # Add the geocode parameter to the query parameters
                self.query_params['geocode'] = geocode

                # Make the API request
                res = requests.get(self.base_url, params=self.query_params).json().get('location')
                #print(res)

                # Extract the PWS station IDs from the API response
                init_candidates = list(zip(res.get('stationName'), res.get('stationId'), res.get('qcStatus'), res.get('latitude'), res.get('longitude')))

                filtered_candidates = [(name, station, value, lat, lon) for (name, station, value, lat, lon) in init_candidates
                            if value == 1 and station.startswith("KNYNEWYO")]
                [self.pws_set.add(cand) for cand in filtered_candidates]
        return self.pws_set


if __name__ == "__main__":
    locator = PWSLocator()
    nyc_pws = locator.get_pws()

    # Print the set of unique PWS station IDs
    for station in nyc_pws:
        print(station)

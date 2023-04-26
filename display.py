import folium

# Define the latitude and longitude of New York City
nyc_lat = 40.7128
nyc_lon = -74.0060

# Create a folium map centered on New York City
m = folium.Map(location=[nyc_lat, nyc_lon], zoom_start=11)

# Define the coordinates of the New York City boundary polygon
ny_lat_lon = [(40.915256, -74.255735), (40.491368, -73.700272), (40.502463, -73.433410), (40.575525, -73.333054), (40.800037, -73.138032), (40.915256, -73.879484), (40.915256, -74.255735)]

# Add the boundary polygon to the map
folium.Polygon(ny_lat_lon, color='red', fill=False).add_to(m)

# Save the map to a file: Double click the file in File Explorer to see the NYC boundary
m.save("nyc_boundaries.html")

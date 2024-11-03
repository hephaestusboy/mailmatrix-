import requests
import math

def get_coordinates(location_name):
    """Get coordinates (latitude, longitude) for a given location name using Nominatim API."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    
    headers = {
        'User-Agent': 'mailmatrix/1.0 (thisisatestmail19@gmail.com)'  # Your app name and email
    }

    response = requests.get(url, params=params, headers=headers)
    print(f"Nominatim API Response: {response.text}")  # Debug print

    if response.status_code == 200 and response.json():
        latitude = float(response.json()[0]['lat'])
        longitude = float(response.json()[0]['lon'])
        return f"{latitude},{longitude}"  # Return in 'lat,lon' format
    else:
        raise Exception("Error fetching coordinates: " + str(response.json()))

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the Haversine distance between two points on the Earth specified in decimal degrees."""
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r  # Return distance in kilometers

def calculate_travel_time(api_key, origin, destination):
    """Calculate travel time using OpenRouteService, with fallback to vector distance if needed."""
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    
    # Parse origin and destination into separate lat/lon components
    origin_lat, origin_lon = map(float, origin.split(','))
    destination_lat, destination_lon = map(float, destination.split(','))

    # Construct the query parameters in the specified format
    query_url = (f"{url}?api_key={api_key}&start={origin_lon},{origin_lat}"
                  f"&end={destination_lon},{destination_lat}")
    print(f"Query URL: {query_url}")  # Display the query URL

    response = requests.get(query_url)  # Use the constructed URL for the request
    print(f"ORS API Response: {response.text}")  # Debug print

    if response.status_code == 200 and 'features' in response.json():
        travel_time = response.json()['features'][0]['properties']['segments'][0]['duration'] / 60  # Convert seconds to minutes
        return travel_time
    else:
        error_message = response.json().get('error', {}).get('message', 'Unknown error')
        print(f"Error fetching travel time: {error_message}")

        # Fallback to vector distance calculation
        distance = haversine(origin_lat, origin_lon, destination_lat, destination_lon)
        average_speed_kmh = 60  # Average speed in km/h
        travel_time = (distance / average_speed_kmh) * 60  # Convert hours to minutes
        print(f"Using vector distance: {distance:.2f} km, estimated travel time: {travel_time:.2f} minutes.")
        return travel_time

def main():
    # Read the API key from the api.txt file
    with open('api.txt', 'r') as file:
        api_key = file.read().strip()  # Read the API key and remove any surrounding whitespace

    # Example of current location (latitude, longitude)
    current_location = "40.7128,-74.0060"  

    # Input destination location name
    destination_name = "Perinthalmanna, India"  

    # Get coordinates for the destination
    try:
        destination_coords = get_coordinates(destination_name)
        
        # Calculate travel time
        travel_time = calculate_travel_time(api_key, current_location, destination_coords)
        print(f"The estimated travel time from current location to {destination_name} is {travel_time:.2f} minutes.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

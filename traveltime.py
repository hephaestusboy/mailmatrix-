import requests
import math
import os

travel_times = []

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

    if response.status_code == 200 and response.json():
        latitude = float(response.json()[0]['lat'])
        longitude = float(response.json()[0]['lon'])
        return f"{latitude},{longitude}"  # Return in 'lat,lon' format
    else:
        raise Exception("Error fetching coordinates: " + str(response.json()))

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the Haversine distance between two points on the Earth specified in decimal degrees."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r  # Return distance in kilometers

def calculate_travel_time(api_key, origin, destination):
    """Calculate travel time using OpenRouteService, with fallback to vector distance if needed."""
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    
    origin_lat, origin_lon = map(float, origin.split(','))
    destination_lat, destination_lon = map(float, destination.split(','))

    query_url = (f"{url}?api_key={api_key}&start={origin_lon},{origin_lat}"
                  f"&end={destination_lon},{destination_lat}")

    response = requests.get(query_url)

    if response.status_code == 200 and 'features' in response.json():
        travel_time = response.json()['features'][0]['properties']['segments'][0]['duration'] / 60  # Convert seconds to minutes
        return float(travel_time)  # Ensure it returns a float
    else:
        # Fallback to vector distance calculation
        distance = haversine(origin_lat, origin_lon, destination_lat, destination_lon)
        average_speed_kmh = 60  # Average speed in km/h
        travel_time = (distance / average_speed_kmh) * 60  # Convert hours to minutes
        return float(travel_time)



def get_current_location():
    """Get the device's current geographical location using IP-based geolocation."""
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            # Split the 'loc' field which is in 'latitude,longitude' format
            return data['loc']
        else:
            raise Exception("Error fetching current location from IP info.")
    except Exception as e:
        print(f"Error retrieving current location: {e}")
        # Set a default location as a fallback if the API call fails
        return "40.7128,-74.0060"  # Example location (New York City)

def get_locations_from_data_file():
    """Retrieve all location entries from data.txt along with the full lines."""
    locations = []
    full_lines = []
    with open('data.txt', 'r') as file:
        for line in file:
            if "Location: " in line:
                location = line.split("Location: ")[1].split(",")[0].strip()
                locations.append(location)
                full_lines.append(line.strip())  # Store the full line for moving later
    return locations, full_lines

def main():
    # Read the API key from the api.txt file
    with open('api.txt', 'r') as file:
        api_key = file.read().strip()

    # Get the device's current location dynamically
    current_location = get_current_location()
    print(f"Current location: {current_location}")

    # Get all destination locations and their corresponding lines from data.txt
    destination_names, full_lines = get_locations_from_data_file()

    global travel_times

    # Calculate and print each travel time for each location entry
    for i, destination_name in enumerate(destination_names):
        try:
            destination_coords = get_coordinates(destination_name)
            travel_time = calculate_travel_time(api_key, current_location, destination_coords)
            travel_times.append(f"{float(travel_time):.2f}")
            
            # Move the processed line to data1.txt
            with open('data1.txt', 'a') as data1_file:
                data1_file.write(full_lines[i] + "\n")

        except Exception as e:
            print(f"Error for {destination_name}: {e}")

    # After processing, update data.txt by removing processed lines
    with open('data.txt', 'r') as file:
        lines = file.readlines()

    with open('data.txt', 'w') as file:
        for line in lines:
            if line.strip() not in full_lines:  # Only keep lines not processed
                file.write(line)


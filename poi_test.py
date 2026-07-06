import requests, json

from mapgame_db import add_resource_group

RESOURCE_DISTANCE_DB = 1000
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
        "User-Agent": "MichaelTestARGame/0.1 (learning project; contact: https://github.com/paulsenm)",
        "Accept": "application/json",
    }
def get_intersections(lat, lon):
    query = f"""
    [out:json][timeout:25];
    node(around:1525,{lat},{lon})[amenity];
    out body;
    """
    
    url = OVERPASS_URL
    
    headers = HEADERS
    
    r = requests.post(url, data={"data": query}, headers=headers)
    
    print("status:", r.status_code)
    results = r.text
    json_resutls = json.loads(results)
    print(json_resutls)
    coord_array = []
    elements = json_resutls.get('elements')
    for node in elements:
        lat = node.get('lat')
        lon = node.get('lon')
        coord_array.append([lat, lon])
    return coord_array

def add_resource_pins_db(lat, lon):
    query = f"""
    [out:json][timeout:25];
    node(around:{RESOURCE_DISTANCE_DB},{lat},{lon})[amenity];
    out body;
    """
    r = requests.post(OVERPASS_URL, data={'data':query}, headers=HEADERS)
    print('status: ', r.status_code)
    response = r.text
    json_results = json.loads(response)
    elements = json_results.get('elements')
    add_resource_group(elements)
    print('added resources to db')



def get_parks(lat, lon):
    query = f"""
    [out:json][timeout:25];
    nwr(around:1000,{lat},{lon})["leisure"];
    out center;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    
    headers = HEADERS
    
    r = requests.post(url, data={"data": query}, headers=headers)
    
    print("status:", r.status_code)
    results = r.text
    json_resutls = json.loads(results)
    park_data = []
    for place in json_resutls['elements']:
        print('begin place data')
        print(f"place data: {place}")
        location = place.get('center')
        tags = place.get('tags', {})
        name = tags.get('name', 'Unnamed park')
        park_data.append([location, name, tags])
        print(f"location: {location}, name: {name}")
    return park_data

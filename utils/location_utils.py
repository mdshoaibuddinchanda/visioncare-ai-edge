"""
Location utility functions for geocoding and distance calculations.
"""
import math


def extract_location_from_input(location_input):
    """
    Extract and standardize location from user input.
    
    Args:
        location_input: Raw location string from user
        
    Returns:
        str: Standardized location string
    """
    if not location_input or not location_input.strip():
        return "New Delhi, India"
    
    location = location_input.strip()
    
    # Handle common abbreviations
    abbreviations = {
        "del": "Delhi",
        "mum": "Mumbai",
        "bom": "Mumbai",
        "blr": "Bangalore",
        "bangalore": "Bengaluru",
        "chn": "Chennai",
        "madras": "Chennai",
        "kol": "Kolkata",
        "calcutta": "Kolkata",
        "hyd": "Hyderabad",
        "secunderabad": "Hyderabad",
        "pun": "Pune",
        "ahm": "Ahmedabad",
        "sur": "Surat",
        "jai": "Jaipur",
        "luck": "Lucknow",
        "kan": "Kanpur",
        "nag": "Nagpur",
        "ind": "Indore",
        "bho": "Bhopal",
        "pat": "Patna",
        "vad": "Vadodara",
        "gha": "Ghaziabad",
        "lud": "Ludhiana",
        "ago": "Agra",
        "nashik": "Nashik",
        "faridabad": "Faridabad",
        "mer": "Meerut",
        "raj": "Rajkot",
        "var": "Varanasi",
        "srinagar": "Srinagar",
        "au": "Aurangabad",
        "dha": "Dhanbad",
        "ami": "Amritsar",
        "nava": "Navi Mumbai",
        "allahabad": "Prayagraj"
    }
    
    lower_loc = location.lower().strip()
    if lower_loc in abbreviations:
        return abbreviations[lower_loc]
    
    # If it's just a single word, assume it's a city in India
    if "," not in location and not any(c.isdigit() for c in location):
        return f"{location.title()}, India"
    
    return location


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula.
    
    Args:
        lat1, lon1: First coordinate
        lat2, lon2: Second coordinate
        
    Returns:
        float: Distance in kilometers
    """
    R = 6371  # Earth's radius in km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def format_distance(distance_km):
    """Format distance in a human-readable way."""
    if distance_km < 1:
        return f"{int(distance_km * 1000)} m"
    elif distance_km < 10:
        return f"{distance_km:.1f} km"
    else:
        return f"{int(distance_km)} km"


def get_nearby_cities(city_name):
    """Get a list of nearby cities for a given Indian city."""
    city_coords = {
        "delhi": (28.7041, 77.1025),
        "mumbai": (19.0760, 72.8777),
        "bangalore": (12.9716, 77.5946),
        "hyderabad": (17.3850, 78.4867),
        "chennai": (13.0827, 80.2707),
        "kolkata": (22.5726, 88.3639),
        "pune": (18.5204, 73.8567),
        "ahmedabad": (23.0225, 72.5714),
        "jaipur": (26.9124, 75.7873),
        "lucknow": (26.8467, 80.9462)
    }
    
    city_lower = city_name.lower().strip()
    if city_lower not in city_coords:
        return []
    
    target_lat, target_lon = city_coords[city_lower]
    
    # Find nearby cities (within 300km)
    nearby = []
    for name, (lat, lon) in city_coords.items():
        if name != city_lower:
            dist = calculate_distance(target_lat, target_lon, lat, lon)
            if dist <= 300:
                nearby.append({"name": name.title(), "distance": round(dist, 1)})
    
    nearby.sort(key=lambda x: x["distance"])
    return nearby[:5]
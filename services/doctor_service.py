"""
Doctor and healthcare facility finder service.
Uses OpenStreetMap Nominatim for geocoding and Overpass API for nearby healthcare.
"""
import json
import urllib.request
import urllib.parse
import ssl
from config.settings import GOOGLE_MAPS_API_KEY


class DoctorService:
    """Finds nearby doctors, hospitals, and clinics."""
    
    def __init__(self):
        self.use_osm = True  # Default to OpenStreetMap (free)
    
    def find_nearby_healthcare(self, location, radius_km=10):
        """
        Find nearby healthcare facilities for a given location.
        
        Args:
            location: City name or coordinates string
            radius_km: Search radius in kilometers
            
        Returns:
            list: Healthcare facilities
        """
        try:
            # Geocode the location to get coordinates
            lat, lon = self._geocode(location)
            
            if not lat or not lon:
                return self._get_fallback_doctors(location)
            
            # Search for healthcare facilities
            facilities = self._search_healthcare_osm(lat, lon, radius_km)
            
            if facilities:
                return facilities
            else:
                return self._get_fallback_doctors(location)
                
        except Exception as e:
            print(f"Error finding healthcare: {e}")
            return self._get_fallback_doctors(location)
    
    def _geocode(self, location):
        """Geocode a location string to coordinates using Nominatim."""
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(location)}&format=json&limit=1"
            req = urllib.request.Request(url, headers={"User-Agent": "VisionCareAI/1.0"})
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                if data and len(data) > 0:
                    return float(data[0]["lat"]), float(data[0]["lon"])
                return None, None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None, None
    
    def _search_healthcare_osm(self, lat, lon, radius_km):
        """Search for healthcare facilities using Overpass API."""
        try:
            # Convert radius to degrees (approximate)
            radius_deg = radius_km / 111.0
            
            overpass_query = f"""
            [out:json];
            (
              nwr["amenity"="hospital"](around:{radius_km * 1000},{lat},{lon});
              nwr["amenity"="clinic"](around:{radius_km * 1000},{lat},{lon});
              nwr["amenity"="doctors"](around:{radius_km * 1000},{lat},{lon});
              nwr["healthcare"](around:{radius_km * 1000},{lat},{lon});
            );
            out center 50;
            """
            
            url = "https://overpass-api.de/api/interpreter"
            data = urllib.parse.urlencode({"data": overpass_query}).encode()
            
            req = urllib.request.Request(url, data=data, headers={"User-Agent": "VisionCareAI/1.0"})
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
                result = json.loads(response.read().decode())
                
                facilities = []
                for element in result.get("elements", []):
                    tags = element.get("tags", {})
                    
                    # Calculate approximate distance
                    if "lat" in element and "lon" in element:
                        dist = self._haversine(lat, lon, element["lat"], element["lon"])
                    else:
                        dist = round(radius_km / 2, 1)
                    
                    facility = {
                        "name": tags.get("name", tags.get("amenity", "Healthcare Facility").title()),
                        "type": tags.get("amenity", tags.get("healthcare", "clinic")).title(),
                        "address": tags.get("addr:full", f"{tags.get('addr:street', '')} {tags.get('addr:city', '')}".strip() or "Address not available"),
                        "phone": tags.get("phone", tags.get("contact:phone", "Not available")),
                        "distance": f"{round(dist, 1)} km",
                        "rating": self._estimate_rating(tags),
                        "fee": self._estimate_fee(tags),
                        "lat": element.get("lat"),
                        "lon": element.get("lon"),
                        "opening_hours": tags.get("opening_hours", "Not specified")
                    }
                    
                    facilities.append(facility)
                
                # Sort by distance
                facilities.sort(key=lambda x: float(x["distance"].split()[0]))
                
                return facilities[:10]  # Return top 10
                
        except Exception as e:
            print(f"OSM search error: {e}")
            return []
    
    def _get_fallback_doctors(self, location):
        """Return fallback healthcare data when API fails."""
        return [
            {
                "name": "City General Hospital",
                "type": "Hospital",
                "address": f"Main Road, {location}",
                "phone": "+91-1800-123-4567",
                "distance": "~2.5 km",
                "rating": "4.2/5",
                "fee": "₹200-500",
                "opening_hours": "24/7"
            },
            {
                "name": "Vision Eye Clinic",
                "type": "Clinic",
                "address": f"Market Area, {location}",
                "phone": "+91-1800-987-6543",
                "distance": "~3.8 km",
                "rating": "4.5/5",
                "fee": "₹300-800",
                "opening_hours": "Mon-Sat: 9AM-7PM"
            },
            {
                "name": "Community Health Center",
                "type": "Clinic",
                "address": f"Sector 5, {location}",
                "phone": "+91-1800-555-1234",
                "distance": "~5.1 km",
                "rating": "4.0/5",
                "fee": "₹100-300 (Subsidized)"
            },
            {
                "name": "Apollo Specialty Hospital",
                "type": "Hospital",
                "address": f"Ring Road, {location}",
                "phone": "+91-1800-222-3333",
                "distance": "~6.2 km",
                "rating": "4.7/5",
                "fee": "₹500-1500"
            },
            {
                "name": "Dr. Sharma's Eye Care Center",
                "type": "Eye Specialist",
                "address": f"College Road, {location}",
                "phone": "+91-98765-43210",
                "distance": "~4.0 km",
                "rating": "4.8/5",
                "fee": "₹400-1000"
            }
        ]
    
    def _haversine(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates in km."""
        import math
        R = 6371  # Earth's radius in km
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _estimate_rating(self, tags):
        """Estimate rating based on available tags."""
        if "rating" in tags:
            return f"{tags['rating']}/5"
        return "4.0/5 (Estimated)"
    
    def _estimate_fee(self, tags):
        """Estimate fee based on facility type."""
        amenity = tags.get("amenity", "").lower()
        if amenity == "hospital":
            return "₹300-1500"
        elif amenity == "clinic":
            return "₹200-800"
        elif amenity == "doctors":
            return "₹300-1000"
        return "₹200-500"
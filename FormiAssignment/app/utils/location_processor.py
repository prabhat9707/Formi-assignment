from groq import Groq
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from fuzzywuzzy import process

GROQ_API_KEY = "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"

# Common Indian cities and locations for fuzzy matching
COMMON_LOCATIONS = [
    "Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad", 
    "Ahmedabad", "Pune", "Jaipur", "Udaipur", "Lucknow", "Kanpur", 
    "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Agra"
]

class LocationProcessor:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.geolocator = Nominatim(user_agent="property_finder")
        
    def correct_spelling(self, location):
        """Correct common spelling mistakes in location names."""
        # First try exact match
        if location in COMMON_LOCATIONS:
            return location
            
        # Try fuzzy matching
        match, score = process.extractOne(location, COMMON_LOCATIONS)
        if score >= 80:  # If similarity is 80% or higher
            print(f"Corrected '{location}' to '{match}'")
            return match
        return location
        
    def extract_location(self, query):
        """Extract location information from user query using Groq."""
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts location information from user queries. Return only the location name in a clean format suitable for geocoding."},
                    {"role": "user", "content": f"Extract the location from this query: {query}"}
                ]
            )
            location = completion.choices[0].message.content.strip()
            return self.correct_spelling(location)
        except Exception as e:
            print(f"Error in Groq API call: {str(e)}")
            return self.correct_spelling(query)  # fallback to original query with spelling correction
            
    def get_coordinates(self, location_name):
        """Convert location name to coordinates using Nominatim."""
        try:
            search_query = f"{location_name}, India"
            location = self.geolocator.geocode(search_query)
            
            if location:
                return {
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'address': location.address
                }
            return None
            
        except GeocoderTimedOut:
            print("Geocoding service timed out")
            return None
        except Exception as e:
            print(f"Error in geocoding: {str(e)}")
            return None 
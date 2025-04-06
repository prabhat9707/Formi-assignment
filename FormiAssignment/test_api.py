import requests
from time import sleep, time

BASE_URL = "http://localhost:5000/api"

def test_search(query, category):
    """
    Make an API request and print the results in a formatted way
    """
    print(f"\n{'='*80}")
    print(f"Testing {category}: '{query}'")
    print('='*80)
    
    try:
        # Start timing
        start_time = time()
        
        # Make API request and measure network time
        request_start = time()
        response = requests.get(f"{BASE_URL}/properties/search", 
                              params={"location": query})
        network_time = time() - request_start
        
        if response.status_code == 200:
            data = response.json()
            
            # Calculate total processing time
            total_time = time() - start_time
            
            print("\n✅ Search Results:")
            print("⏱️  Response Time:")
            print(f"   • API Request: {network_time:.2f}s")
            print(f"   • Total Processing: {total_time:.2f}s")
            print(f"\n📍 Search Location: {data['search_location']['name']}")
            print(f"🌍 Resolved Address: {data['search_location']['resolved_address']}")
            print(f"📌 Coordinates: {data['search_location']['coordinates']}")
            print(f"🏠 Properties found: {data['count']}\n")
            
            if data['count'] > 0:
                print("Top 3 nearest properties:")
                for idx, prop in enumerate(data['properties'][:3], 1):
                    print(f"\n{idx}. {prop['name']}")
                    print(f"   Distance: {prop['distance']:.2f} km")
                    print(f"   Address: {prop['address']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Add delay to prevent overwhelming the geocoding service
    sleep(1)

def run_tests():
    """
    Run a series of test cases covering different search scenarios
    """
    
    # Track overall test execution time
    overall_start = time()
    
    # 1. Simple city searches (including misspellings)
    city_tests = [
        "Udaipur",
        "Delih",  # Misspelled
        "bangalre",  # Misspelled
        "Mumbai"
    ]
    
    # 2. Area-based searches
    area_tests = [
        "Lake Palace area in Udaipur",
        "Bandra West Mumbai",
        "South Delhi",
        "Electronic City Bangalore"
    ]
    
    # 3. Landmark-based searches
    landmark_tests = [
        "near City Palace Udaipur",
        "close to India Gate Delhi",
        "near Gateway of India Mumbai",
        "around Mysore Palace"
    ]
    
    # 4. Complex queries
    complex_tests = [
        "hotels near bangalore airport",
        "properties within 5km of Taj Mahal",
        "residential areas near Marine Drive Mumbai",
        "guest houses in old city udaipur"
    ]
    
    # Run all tests
    print("\nStarting API Tests...\n")
    
    print("\n🏙️  Testing City Searches")
    for query in city_tests:
        test_search(query, "City Search")
        
    print("\n📍 Testing Area Searches")
    for query in area_tests:
        test_search(query, "Area Search")
        
    print("\n🏛️  Testing Landmark Searches")
    for query in landmark_tests:
        test_search(query, "Landmark Search")
        
    print("\n🔍 Testing Complex Queries")
    for query in complex_tests:
        test_search(query, "Complex Query")
    
    # Print overall execution time
    total_execution = time() - overall_start
    print(f"\n{'='*80}")
    print(f"Total Test Execution Time: {total_execution:.2f}s")
    print(f"Average Time per Query: {total_execution/len(city_tests + area_tests + landmark_tests + complex_tests):.2f}s")
    print('='*80)

if __name__ == "__main__":
    run_tests() 
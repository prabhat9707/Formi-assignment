# Property Search API

A Flask-based API service that helps find properties within a 50km radius of a given location in India. The service supports natural language queries and handles common spelling mistakes in location names.

## Features

- 🔍 Natural language location search
- 🗺️ Geocoding support for Indian locations
- ✍️ Spelling mistake tolerance for city names
- 📏 50km radius property search
- 📊 Distance-based result sorting
- ⏱️ Performance metrics

## Prerequisites

- Python 3.8+
- Groq API key (for natural language processing)
- Internet connection (for geocoding service)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Groq API key:
   - Get your API key from [Groq](https://console.groq.com)
   - Update the `GROQ_API_KEY` in `app/utils/location_processor.py`

## Importing Property Data

The application requires a SQLite database (`properties.db`) containing property information. To create this database from the provided PDF:

1. Ensure you have the property data PDF file named `List_of_Properties_with_Location.pdf` in your project root directory.

2. Run the import script:
```bash
python import_data.py
```

The script will:
- Create a new SQLite database (`properties.db`)
- Extract property information from the PDF
- Parse location coordinates and property details
- Import the data into the database

Expected PDF format:
```
Property Name 1 latitude1 longitude1
Property Address Line 1
Property Address Line 2

Property Name 2 latitude2 longitude2
Property Address Line 1
Property Address Line 2
```

Example:
```
Moustache Udaipur Luxuria 24.57799888 73.68263271
Near Fateh Sagar Lake, Udaipur
Rajasthan, India
```

The import script handles:
- Property name extraction
- Coordinate parsing
- Address compilation
- Data validation
- Error reporting

You can verify the import by checking:
1. The console output for import statistics
2. Using the `/api/properties` endpoint to list all imported properties
```bash
# Get all properties
curl "http://localhost:5000/api/properties"
```
3. The SQLite database directly using any SQLite browser

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── property.py
│   ├── routes/
│   │   └── api.py
│   └── utils/
│       └── location_processor.py
├── requirements.txt
├── run.py
└── test_api.py
```

## Running the Application

1. Start the Flask server:
```bash
python run.py
```

2. The API will be available at `http://localhost:5000`

## API Endpoints

### GET /api/properties/search
Search for properties near a location.

**Parameters:**
- `location` (string): Natural language location query

**Example Requests:**
```bash
# Simple city search
curl "http://localhost:5000/api/properties/search?location=Udaipur"

# Area search
curl "http://localhost:5000/api/properties/search?location=Bandra West Mumbai"

# Landmark search
curl "http://localhost:5000/api/properties/search?location=near Gateway of India"
```

**Response Format:**
```json
{
    "search_location": {
        "name": "Udaipur",
        "coordinates": [24.5854, 73.7125],
        "resolved_address": "Udaipur, Rajasthan, India"
    },
    "count": 5,
    "properties": [
        {    
            "id" : "id"
            "name": "Property Name",
            "distance": 2.5,
            "address": "Property Address",
            "latitude": 24.5854,
            "longitude": 73.7125
        }
    ]
}
```

## Running Tests

The project includes a comprehensive test suite that checks various search scenarios:

```bash
python test_api.py
```

The test suite covers:
1. Simple city searches (including misspellings)
2. Area-based searches
3. Landmark-based searches
4. Complex queries

Each test provides:
- Response times (API request and total processing)
- Search results with coordinates
- Top 3 nearest properties
- Distance information

## Performance Metrics

The test suite provides detailed timing information:
- API request time
- Total processing time per query
- Overall test execution time
- Average time per query

## Error Handling

The API handles various error cases:
- Invalid location queries
- Geocoding failures
- API timeouts
- Spelling mistakes in city names
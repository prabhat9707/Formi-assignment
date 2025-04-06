from flask import Blueprint, jsonify, request
from app.models.property import Property
from geopy.distance import geodesic
from app.utils.location_processor import LocationProcessor
from urllib.parse import unquote

bp = Blueprint('api', __name__, url_prefix='/api')
location_processor = LocationProcessor()

@bp.route('/properties/search', methods=['GET'])
def search_properties():
    try:
        # Get location query from request and decode it
        location_query = request.args.get('location', '')
        location_query = unquote(location_query)  # Decode URL-encoded string

        print(location_query)
        
        if not location_query:
            return jsonify({'error': 'Location query is required'}), 400
            
        # Extract location from query
        location_name = location_processor.extract_location(location_query)
        print(f"Searching for location: {location_name}")
        
        # Get coordinates for the location
        location_data = location_processor.get_coordinates(location_name)
        if not location_data:
            return jsonify({
                'error': f'Could not find coordinates for location: {location_name}',
                'query' : location_query
            }), 404
            
        # Get all properties
        properties = Property.query.all()
        
        # Calculate distances and filter properties within 50km
        result = []
        search_point = (location_data['latitude'], location_data['longitude'])
        
        for property in properties:
            property_point = (property.latitude, property.longitude)
            distance = geodesic(search_point, property_point).kilometers
            
            if distance <= 50:
                property_dict = property.to_dict()
                property_dict['distance'] = round(distance, 2)
                result.append(property_dict)
        
        # Sort by distance
        result.sort(key=lambda x: x['distance'])
        
        return jsonify({
            'search_location': {
                'name': location_name,
                'coordinates': search_point,
                'resolved_address': location_data['address']
            },
            'count': len(result),
            'properties': result,
            'query' : location_query
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/properties', methods=['GET'])
def get_all_properties():
    properties = Property.query.all()
    return jsonify({
        'count': len(properties),
        'properties': [p.to_dict() for p in properties]
    }) 
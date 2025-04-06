import PyPDF2
from app import create_app, db
from app.models.property import Property
import re

def extract_properties_from_pdf(pdf_path):
    properties_data = []
    
    try:
        with open(pdf_path, 'rb') as file:
            # Create PDF reader object
            print("How are you")
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Split text into lines and process each line
            lines = text.split('\n')
            print(lines)
            
            # Regular expression pattern for coordinates - matches two numbers separated by space
            coord_pattern = r'(\d+\.\d+)\s+(\d+\.\d+)'
            
            current_property = {}
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Look for coordinates in the line
                coord_match = re.search(coord_pattern, line)
                print(coord_match)
                if coord_match:
                    # If we have a previous property, save it
                    if current_property:
                        properties_data.append(current_property)
                    
                    # Start a new property
                    lat, lon = coord_match.groups()
                    print(lat, lon)
                    # Extract name by taking everything before the coordinates
                    name = line[:line.find(lat)].strip()
                    current_property = {
                        'latitude': float(lat),
                        'longitude': float(lon),
                        'name': name,
                        'address': ''
                    }
                elif current_property:
                    # Append to address if we have a current property
                    current_property['address'] = (current_property['address'] + ' ' + line).strip()
            
            # Don't forget to add the last property
            if current_property:
                properties_data.append(current_property)
                
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return []
    
    return properties_data

def import_properties():
    app = create_app()
    with app.app_context():
        try:
            # Read properties from PDF
            properties_data = extract_properties_from_pdf('List_of_Properties_with_Location.pdf')
            
            if not properties_data:
                print("No properties found in the PDF!")
                return
            
            # Clear existing data
            Property.query.delete()
            
            # Import new data
            for data in properties_data:
                property = Property.from_dict(data)
                db.session.add(property)
            
            db.session.commit()
            print(f"Successfully imported {len(properties_data)} properties!")
            
        except Exception as e:
            print(f"Error importing data: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    import_properties() 
from app import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address
        }
    
    @staticmethod
    def from_dict(data):
        return Property(
            name=data.get('name'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            address=data.get('address')
        ) 
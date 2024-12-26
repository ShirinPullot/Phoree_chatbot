# Combined property store with UI-friendly data
property_store = {
    "Dubai Hills": {
        "villa": [
            {
                "title": "Luxury Villa in Dubai Hills",
                "price": "AED 4.8M",
                "bedrooms": 4,
                "bathrooms": 5,
                "area": "4,500 sq ft",
                "features": ["Spacious Garden", "Private Pool", "Smart Home", "Modern Kitchen"],
                "image": "/dubai-hills-villa.jpg"  # Add actual image path
            },
            {
                "title": "Premium Villa with Pool",
                "price": "AED 5M",
                "bedrooms": 5,
                "bathrooms": 6,
                "area": "5,000 sq ft",
                "features": ["Swimming Pool", "Garden", "Smart Home", "Gym"],
                "image": "/dubai-hills-premium.jpg"  # Add actual image path
            }
        ]
    },
    "Dubai Marina": {
        "apartment": [
            {
                "title": "Marina View Apartment",
                "price": "AED 2.5M",
                "bedrooms": 2,
                "bathrooms": 3,
                "area": "1,800 sq ft",
                "features": ["Marina View", "Fully Furnished", "Balcony", "Gym Access"],
                "image": "/marina-view.jpg"  # Add actual image path
            },
            {
                "title": "Luxury Marina Penthouse",
                "price": "AED 4.2M",
                "bedrooms": 3,
                "bathrooms": 4,
                "area": "2,500 sq ft",
                "features": ["Panoramic View", "Private Terrace", "Smart Home", "Premium Finishes"],
                "image": "/marina-penthouse.jpg"  # Add actual image path
            }
        ],
        "townhouse": [
            {
                "title": "Marina Walk Townhouse",
                "price": "AED 4.5M",
                "bedrooms": 3,
                "bathrooms": 4,
                "area": "3,200 sq ft",
                "features": ["Rooftop Terrace", "Private Garden", "Walk to Beach", "Modern Design"],
                "image": "/marina-townhouse.jpg"  # Add actual image path
            }
        ]
    },
    "Palm Jumeirah": {
        "apartment": [
            {
                "title": "Sea View Palm Apartment",
                "price": "AED 3.5M",
                "bedrooms": 2,
                "bathrooms": 3,
                "area": "2,000 sq ft",
                "features": ["Sea View", "Private Beach Access", "Infinity Pool", "Luxury Finishes"],
                "image": "/palm-apartment.jpg"  # Add actual image path
            }
        ]
    }
}

async def get_properties(location: str = None, property_type: str = None, max_price: float = None) -> list:
    filtered_properties = []
    
    for loc, properties in property_store.items():
        if location and location.lower() != loc.lower():
            continue
        
        for prop_type, listings in properties.items():
            if property_type and property_type.lower() != prop_type.lower():
                continue
            
            for listing in listings:
                price = float(listing['price'].replace('AED ', '').replace('M', ''))
                if max_price and price > max_price:
                    continue
                
                filtered_properties.append({
                    "location": loc,
                    "type": prop_type,
                    **listing
                })
    
    return filtered_properties

async def add_property(location: str, property_type: str, property_data: dict):
    if location not in property_store:
        property_store[location] = {}
    
    if property_type not in property_store[location]:
        property_store[location][property_type] = []
    
    property_store[location][property_type].append(property_data)
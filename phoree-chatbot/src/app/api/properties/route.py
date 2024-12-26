from fastapi import FastAPI
from src.lib.document_store import get_properties
app = FastAPI()

@app.get("/api/properties")
async def get_properties():
    # Get first property from document_store for demo
    first_location = next(iter(property_store))
    first_type = next(iter(property_store[first_location]))
    properties = property_store[first_location][first_type]
    
    return {"properties": properties} 
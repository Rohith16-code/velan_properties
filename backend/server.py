from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Import models
from models import (
    Contact, ContactCreate, ContactResponse,
    Property, PropertyCreate, PropertyUpdate, PropertyResponse
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
contacts_collection = db.contacts
properties_collection = db.properties

# Create the main app without a prefix
app = FastAPI(title="Velan Properties API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Health Check
@api_router.get("/")
async def root():
    return {"message": "Velan Properties API is running", "status": "healthy"}

# Contact Endpoints
@api_router.post("/contacts", response_model=ContactResponse)
async def create_contact(contact_data: ContactCreate):
    try:
        # Create contact object
        contact = Contact(**contact_data.dict())
        
        # Insert into database
        result = await contacts_collection.insert_one(contact.dict())
        
        if result.inserted_id:
            logger.info(f"New contact created: {contact.id} - {contact.name}")
            return ContactResponse(
                success=True,
                message="Thank you for your inquiry! We will contact you soon.",
                contact_id=contact.id
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save contact")
            
    except Exception as e:
        logger.error(f"Error creating contact: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/contacts", response_model=List[Contact])
async def get_contacts(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None)
):
    try:
        # Build query
        query = {}
        if status:
            query["status"] = status
            
        # Get contacts with pagination
        cursor = contacts_collection.find(query).sort("created_at", -1).skip(offset).limit(limit)
        contacts = await cursor.to_list(length=limit)
        
        return [Contact(**contact) for contact in contacts]
        
    except Exception as e:
        logger.error(f"Error fetching contacts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Property Endpoints
@api_router.get("/properties", response_model=List[Property])
async def get_properties(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query("active")
):
    try:
        # Build query
        query = {}
        if status:
            query["status"] = status
        if type:
            query["type"] = type
            
        # Get properties with pagination
        cursor = properties_collection.find(query).sort("created_at", -1).skip(offset).limit(limit)
        properties = await cursor.to_list(length=limit)
        
        return [Property(**property) for property in properties]
        
    except Exception as e:
        logger.error(f"Error fetching properties: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.post("/properties", response_model=PropertyResponse)
async def create_property(property_data: PropertyCreate):
    try:
        # Create property object
        property_obj = Property(**property_data.dict())
        
        # Insert into database
        result = await properties_collection.insert_one(property_obj.dict())
        
        if result.inserted_id:
            logger.info(f"New property created: {property_obj.id} - {property_obj.title}")
            return PropertyResponse(
                success=True,
                message="Property created successfully",
                property_id=property_obj.id
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save property")
            
    except Exception as e:
        logger.error(f"Error creating property: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.put("/properties/{property_id}", response_model=PropertyResponse)
async def update_property(property_id: str, property_data: PropertyUpdate):
    try:
        # Build update data
        update_data = {k: v for k, v in property_data.dict().items() if v is not None}
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
        
        # Update property
        result = await properties_collection.update_one(
            {"id": property_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Property not found")
        elif result.modified_count == 0:
            return PropertyResponse(
                success=True,
                message="No changes made to property",
                property_id=property_id
            )
        else:
            logger.info(f"Property updated: {property_id}")
            return PropertyResponse(
                success=True,
                message="Property updated successfully",
                property_id=property_id
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating property: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.delete("/properties/{property_id}")
async def delete_property(property_id: str):
    try:
        # Delete property
        result = await properties_collection.delete_one({"id": property_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Property not found")
        else:
            logger.info(f"Property deleted: {property_id}")
            return {"success": True, "message": "Property deleted successfully"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting property: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Admin Dashboard Stats (Future feature)
@api_router.get("/admin/dashboard")
async def get_dashboard_stats():
    try:
        # Count documents
        total_contacts = await contacts_collection.count_documents({})
        new_contacts = await contacts_collection.count_documents({"status": "new"})
        total_properties = await properties_collection.count_documents({})
        active_properties = await properties_collection.count_documents({"status": "active"})
        
        return {
            "contacts": {
                "total": total_contacts,
                "new": new_contacts
            },
            "properties": {
                "total": total_properties,
                "active": active_properties
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching dashboard stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Velan Properties API starting up...")
    # Initialize with sample properties if none exist
    count = await properties_collection.count_documents({})
    if count == 0:
        logger.info("Initializing with sample properties...")
        sample_properties = [
            {
                "id": "sample-1",
                "title": "Modern Family Villa",
                "price": "₹45,00,000",
                "location": "Hosur Main Road, TamilNadu",
                "bedrooms": 4,
                "parking": 2,
                "area": "2,800 sq ft",
                "type": "For Sale",
                "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
                "description": "Beautiful modern villa with all amenities",
                "features": ["Swimming Pool", "Garden", "Security", "Power Backup"],
                "status": "active",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": "sample-2", 
                "title": "Luxury Apartment",
                "price": "₹22,000/month",
                "location": "Hosur City Center, TamilNadu",
                "bedrooms": 2,
                "parking": 1,
                "area": "1,200 sq ft",
                "type": "For Rent",
                "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80",
                "description": "Premium apartment in prime location",
                "features": ["Gym", "Security", "Parking", "Balcony"],
                "status": "active",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": "sample-3",
                "title": "Cozy Suburban Home", 
                "price": "₹32,00,000",
                "location": "Bagalur Road, Hosur",
                "bedrooms": 3,
                "parking": 2,
                "area": "2,100 sq ft",
                "type": "For Sale",
                "image": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=800&q=80",
                "description": "Perfect family home in quiet neighborhood",
                "features": ["Garden", "Security", "School Nearby", "Park"],
                "status": "active",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        await properties_collection.insert_many(sample_properties)
        logger.info("Sample properties initialized")

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Velan Properties API shutting down...")
    client.close()
# API Contracts - Velan Properties

## Overview
This document defines the API contracts for integrating the Velan Properties frontend with the backend services.

## Current Mock Data (to be replaced)
- **Location**: `/app/frontend/src/data/mockData.js`
- **Mock Properties**: 6 sample properties with images, pricing, locations, etc.
- **Contact Form**: Currently shows alert on submission

## Backend Implementation Requirements

### 1. Database Models

#### Contact Model
```python
class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="new")  # new, contacted, resolved
```

#### Property Model  
```python
class Property(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    price: str
    location: str
    bedrooms: int
    parking: int
    area: str
    type: str  # For Sale, For Rent, Investment
    image: str
    description: Optional[str] = None
    features: Optional[List[str]] = None
    status: str = Field(default="active")  # active, sold, rented
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2. API Endpoints to Implement

#### Contact Endpoints
- **POST /api/contacts** - Submit contact form
  - Input: name, email, phone (optional), message
  - Output: success message, contact_id
  - Action: Save to database, send notification

- **GET /api/contacts** - Get all contacts (admin)
  - Output: List of all contacts
  - Pagination: limit, offset

#### Property Endpoints
- **GET /api/properties** - Get all active properties
  - Output: List of properties for public display
  - Filters: type, price_range, location
  
- **POST /api/properties** - Create new property (admin)
  - Input: Property data
  - Output: Created property with ID
  
- **PUT /api/properties/{property_id}** - Update property (admin)
  - Input: Property data to update
  - Output: Updated property
  
- **DELETE /api/properties/{property_id}** - Delete property (admin)
  - Output: Success message

#### Admin Endpoints (Future)
- **GET /api/admin/dashboard** - Admin dashboard stats
- **GET /api/admin/contacts** - Manage contacts
- **GET /api/admin/properties** - Manage properties

### 3. Frontend Integration Points

#### Contact Form (HomePage.js)
- **Current**: `handleFormSubmit` shows alert
- **Update**: POST to `/api/contacts` endpoint
- **Success**: Show toast notification
- **Error**: Display error message

#### Properties Section (HomePage.js)  
- **Current**: Uses `mockProperties` from mockData.js
- **Update**: Fetch from `/api/properties` on component mount
- **Loading**: Show skeleton/loading state
- **Error**: Display error message

#### Admin Features (Future)
- Property management dashboard
- Contact management system
- Add/Edit property forms

### 4. Contact Information Updates
- **WhatsApp Number**: Update to +919443246742
- **Email**: Update to velanproperties777@gmail.com  
- **Location**: Update to Hosur, TamilNadu - 635126

### 5. Error Handling
- Validation errors for form inputs
- Database connection errors
- Network timeout handling
- User-friendly error messages

### 6. Success Notifications
- Contact form submission success
- Property actions (admin)
- Toast notifications using existing toast system

### 7. Integration Steps
1. Implement backend models and endpoints
2. Update contact information in frontend
3. Replace mock data with API calls
4. Add loading states and error handling
5. Test all functionality
6. Add admin features (optional)

## Notes
- Use existing shadcn toast system for notifications
- Maintain current design and user experience
- All API endpoints should follow /api prefix for proper routing
- Database operations should use existing MongoDB connection
- Form validation should be handled both frontend and backend
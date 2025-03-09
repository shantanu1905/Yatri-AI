from pydantic import BaseModel
from typing import List, Optional
import datetime as dt

# Schema for trip creation (Request)
class TripCreate(BaseModel):
    session_id: str  # Added session_id to match the database schema
    destination: str
    startdate: str  # Updated to match the database column name
    enddate: str  # Updated to match the database column name
    budget: Optional[float] = None  # Made optional to align with the database
    travelers: str  # "Solo", "Couple", "Family", "Friends"
    activities: List[str]  # Sent as a list, stored as comma-separated values in DB

    class Config:
        orm_mode = True

# Define a request model to accept JSON input
class SessionRequest(BaseModel):
    session_id: str

# Schema for returning trip data (Response)
class TripResponse1(BaseModel):
    id: int
    session_id: str
    destination: str
    startdate: str  # Updated to match the database column name
    enddate: str  # Updated to match the database column name
    budget: Optional[float] = None  # Made optional
    travelers: str
    activities: List[str]  # Convert comma-separated values to a list
    created_at: dt.datetime

    class Config:
        orm_mode = True







class AttractionResponse(BaseModel):
    place_name: str
    description: str
    best_time_to_visit: Optional[str] = None
    nearby_points_of_interest: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    display_name: Optional[str] = None

class ItineraryResponse(BaseModel):
    location_name: str
    location_description: str
    ideal_visit_time: Optional[str] = None
    attractions: List[AttractionResponse]

# Schema for returning trip data (Response)
class TripResponse(BaseModel):
    itinerary: Optional[ItineraryResponse]  # ✅ Added itinerary here!

    class Config:
        orm_mode = True



# Define Attraction model
class Attraction(BaseModel):
    place_name: str
    description: str
    best_time_to_visit: str
    nearby_points_of_interest: Optional[str]

# Updated TravelPlan model without day-wise grouping
class TravelPlan(BaseModel):
    location_name: str
    location_description: str
    ideal_visit_time: str
    itinerary: List[Attraction]  # Direct list of attractions (No day-wise grouping)
    other_stuff_to_do: List[str]
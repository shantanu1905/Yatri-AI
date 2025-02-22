from pydantic import BaseModel
from typing import List, Optional
import datetime as dt

# Schema for trip creation (Request)
class TripCreate(BaseModel):
    destination: str
    date: str
    days: int
    budget: float
    travelers: str  # "Solo", "Couple", "Family", "Friends"
    activities: List[str]  # Sent as a list, stored as comma-separated values in DB

    class Config:
        orm_mode = True


# Define a request model to accept JSON input
class SessionRequest(BaseModel):
    session_id: str

    
# Schema for returning trip data (Response)
class TripResponse(BaseModel):
    id: int
    session_id: str
    destination: str
    date: str
    days: int
    budget: float
    travelers: str
    activities: List[str]  # Convert comma-separated values to a list
    created_at: dt.datetime

    class Config:
        orm_mode = True
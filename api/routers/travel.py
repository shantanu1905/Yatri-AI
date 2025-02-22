from fastapi import APIRouter, Depends, Response, Cookie, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from api.database import get_db
from api.models import Trip
from api.schemas import TripCreate, TripResponse, SessionRequest
import datetime as dt

router = APIRouter(prefix="/trips", tags=["Trips"])

# Middleware to generate/get session ID
def get_session_id(session_id: str = Cookie(None)):
    return session_id or str(uuid4())


# Save a trip
@router.post("/", response_model=TripResponse)
def save_trip(
    trip: TripCreate,
    response: Response,
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id)
):
    new_trip = Trip(
        session_id=session_id,
        destination=trip.destination,
        date=trip.date,
        days=trip.days,
        budget=trip.budget,
        travelers=trip.travelers,
        activities=",".join(trip.activities),  # Convert list to a comma-separated string
        created_at=dt.datetime.utcnow()
    )
    
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    response.set_cookie("session_id", session_id)  # Store session ID in cookies

    # Convert activities from comma-separated string to list before returning
    return TripResponse(
        id=new_trip.id,
        session_id=new_trip.session_id,
        destination=new_trip.destination,
        date=new_trip.date,
        days=new_trip.days,
        budget=new_trip.budget,
        travelers=new_trip.travelers,
        activities=new_trip.activities.split(","),  # Convert back to list
        created_at=new_trip.created_at
    )











# Get all trips for a session (session_id from UI JSON request)
@router.post("/savedtrips", response_model=list[TripResponse])
def get_trips(
    request: SessionRequest,  # Accept session_id as JSON
    db: Session = Depends(get_db)
):
    trips = db.query(Trip).filter(Trip.session_id == request.session_id).all()

    if not trips:
        raise HTTPException(status_code=404, detail="No trips found for this session ID")

    # ✅ Convert activities field from string to list if necessary
    for trip in trips:
        if isinstance(trip.activities, str):  # Check if activities is stored as a string
            trip.activities = trip.activities.split(", ")  # Convert string to list

    return trips






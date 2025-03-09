from fastapi import APIRouter, Depends, Response, Cookie, HTTPException

from uuid import uuid4
import datetime as dt
import os
from api.functions import get_location_info

# Database Imports
from api.database import get_db
from sqlalchemy.orm import Session
from api.models import Trip,  Itinerary, Attraction, Flags
from api.schemas import TripCreate, TripResponse, SessionRequest, TripResponse1

# AI Agent Imports
from crewai import Crew, Process
from api.agents import tourist_guide
from api.tasks import places_task



router = APIRouter(prefix="/trips", tags=["Trips"])
# Verify API Key is loaded
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is missing. Check your .env file.")

# Middleware to generate/get session ID
def get_session_id(session_id: str = Cookie(None)):
    return session_id or str(uuid4())


# Save a trip
@router.post("/", response_model=TripResponse1)
def save_trip(
    trip: TripCreate,
    response: Response,
    db: Session = Depends(get_db),
    session_id: str = Depends(get_session_id)
):
    new_trip = Trip(
        session_id=session_id,
        destination=trip.destination,
        startdate=trip.startdate,  # Updated field name
        enddate=trip.enddate,  # Updated field name
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
    return TripResponse1(
        id=new_trip.id,
        session_id=new_trip.session_id,
        destination=new_trip.destination,
        startdate=new_trip.startdate,  # Updated field name
        enddate=new_trip.enddate,  # Updated field name
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
            trip.activities = trip.activities.split(",")  # Convert string to list

    return trips

# ✅ Generate AI Itinerary, Save to DB & Return Results
@router.post("/generateitinerary", response_model=TripResponse)
def generate_itinerary(request: SessionRequest, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.session_id == request.session_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="No trip found for this session ID")

    # ✅ Check if AI-generated itinerary already exists
    flag = db.query(Flags).filter(Flags.trip_id == trip.id).first()

    if flag and flag.ai_generated:
        # ✅ Fetch saved itinerary from DB
        itinerary = db.query(Itinerary).filter(Itinerary.trip_id == trip.id).first()

        if not itinerary:
            raise HTTPException(status_code=500, detail="Itinerary flag exists but no itinerary found!")

        attractions = db.query(Attraction).filter(Attraction.itinerary_id == itinerary.id).all()
        

        return TripResponse(
        
            itinerary={
                "location_name": itinerary.location_name,
                "location_description": itinerary.location_description,
                "ideal_visit_time": itinerary.ideal_visit_time,
                "attractions": [
                    {
                        "place_name": attr.place_name,
                        "description": attr.description,
                        "best_time_to_visit": attr.best_time_to_visit,
                        "nearby_points_of_interest": attr.nearby_points_of_interest,
                        "latitude": attr.latitude,
                        "longitude": attr.longitude,
                        "display_name": attr.display_name,
                    }
                    for attr in attractions
                ],
            },
        )

    # ✅ Prepare input for AI Agent
    trip_inputs = {
        "destination": trip.destination,
        "start_date": trip.startdate,
        "end_date": trip.enddate,
        "budget": trip.budget,
        "traveler_type": trip.travelers,
        "activities": trip.activities.split(","),
    }

    # ✅ Run AI agent (CrewAI)
    crew = Crew(
        agents=[tourist_guide],
        tasks=[places_task],
        process=Process.sequential,
    )

    result = crew.kickoff(inputs=trip_inputs)

    if not result:
        raise HTTPException(status_code=500, detail="AI agent failed to generate an itinerary")

    # ✅ Save Itinerary
    new_itinerary = Itinerary(
        trip_id=trip.id,
        location_name=result["location_name"],
        location_description=result["location_description"],
        ideal_visit_time=result["ideal_visit_time"],
    )
    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)

    # ✅ Save Attractions
    for attraction_data in result["itinerary"]:
        location = get_location_info(attraction_data["place_name"])

        new_attraction = Attraction(
            itinerary_id=new_itinerary.id,
            place_name=attraction_data["place_name"],
            description=attraction_data["description"],
            best_time_to_visit=attraction_data["best_time_to_visit"],
            nearby_points_of_interest=attraction_data["nearby_points_of_interest"],
            latitude=location.get("latitude"),
            longitude=location.get("longitude"),
            display_name=location.get("title"),
        )
        db.add(new_attraction)

    # ✅ Save AI Generation Flag
    new_flag = Flags(
        trip_id=trip.id,
        ai_generated=True,
        user_ip="0.0.0.0",  # Capture user IP
    )
    db.add(new_flag)
    
    db.commit()  # Final commit after all inserts

    # ✅ Return Trip + Itinerary
    return TripResponse(
        itinerary={
            "location_name": new_itinerary.location_name,
            "location_description": new_itinerary.location_description,
            "ideal_visit_time": new_itinerary.ideal_visit_time,
            "attractions": [
                {
                    "place_name": attr.place_name,
                    "description": attr.description,
                    "best_time_to_visit": attr.best_time_to_visit,
                    "nearby_points_of_interest": attr.nearby_points_of_interest,
                    "latitude": attr.latitude,
                    "longitude": attr.longitude,
                    "display_name": attr.display_name,
                }
                for attr in db.query(Attraction).filter(Attraction.itinerary_id == new_itinerary.id).all()
            ],
        },
    )
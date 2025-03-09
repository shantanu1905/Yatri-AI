import datetime as dt
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from api.database import Base


# ✅ Trip Model
class Trip(Base):
    __tablename__ = "trips"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    session_id = sa.Column(sa.String, index=True, nullable=False)
    destination = sa.Column(sa.String, nullable=False)
    startdate = sa.Column(sa.String, nullable=False)
    enddate = sa.Column(sa.String, nullable=False)
    budget = sa.Column(sa.Float, nullable=True)
    travelers = sa.Column(sa.String, nullable=False)  # Solo, Couple, Family, Friends
    activities = sa.Column(sa.String, nullable=False)  # Stored as comma-separated string
    created_at = sa.Column(sa.DateTime, default=dt.datetime.utcnow)

    # ✅ Relationship: A Trip has one Itinerary
    itinerary = relationship("Itinerary", back_populates="trip", uselist=False, cascade="all, delete-orphan")

    # ✅ Relationship: A Trip has one Flag
    flags = relationship("Flags", back_populates="trip", uselist=False, cascade="all, delete-orphan")



# ✅ Itinerary Model (Now Directly Holds Attractions Instead of Day-wise Grouping)
class Itinerary(Base):
    __tablename__ = "itineraries"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    trip_id = sa.Column(sa.Integer, sa.ForeignKey("trips.id"), nullable=False)
    location_name = sa.Column(sa.String, nullable=False)
    location_description = sa.Column(sa.Text, nullable=False)
    ideal_visit_time = sa.Column(sa.String, nullable=False)

    # ✅ Relationship: An Itinerary belongs to a Trip
    trip = relationship("Trip", back_populates="itinerary")

    # ✅ Relationship: An Itinerary directly holds multiple Attractions
    attractions = relationship("Attraction", back_populates="itinerary", cascade="all, delete-orphan")


# ✅ Attraction Model (Now Directly Related to Itinerary)
class Attraction(Base):
    __tablename__ = "attractions"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    itinerary_id = sa.Column(sa.Integer, sa.ForeignKey("itineraries.id"), nullable=False)
    place_name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    best_time_to_visit = sa.Column(sa.String, nullable=True)
    nearby_points_of_interest = sa.Column(sa.String, nullable=True)
    latitude = sa.Column(sa.Float, nullable=True)
    longitude = sa.Column(sa.Float, nullable=True)
    display_name = sa.Column(sa.String, nullable=True)

    # ✅ Relationship: An Attraction belongs to an Itinerary (NOT a day anymore)
    itinerary = relationship("Itinerary", back_populates="attractions")


class Flags(Base):
    __tablename__ = "flags"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    trip_id = sa.Column(sa.Integer, sa.ForeignKey("trips.id"), nullable=False, unique=True)
    ai_generated = sa.Column(sa.Boolean, default=False, nullable=False)  # True if itinerary was AI-generated
    user_ip = sa.Column(sa.String, nullable=True)  # Stores user's IP address
    created_at = sa.Column(sa.DateTime, default=dt.datetime.utcnow)

    # ✅ Relationship: Flags belongs to a Trip
    trip = relationship("Trip", back_populates="flags")
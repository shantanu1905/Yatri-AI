import api.database as _database
import datetime as dt
import sqlalchemy as sa
from api.database import Base

_database.Base.metadata.create_all(_database.engine)

class Trip(Base):
    __tablename__ = "trips"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    session_id = sa.Column(sa.String, index=True, nullable=False)  # Stores session ID for tracking
    destination = sa.Column(sa.String, nullable=False)
    date = sa.Column(sa.String, nullable=False)
    days = sa.Column(sa.Integer, nullable=False)
    budget = sa.Column(sa.Float, nullable=False)
    travelers = sa.Column(sa.String, nullable=False)  # Solo, Couple, Family, Friends
    activities = sa.Column(sa.String, nullable=False)  # Stored as a comma-separated string
    created_at = sa.Column(sa.DateTime, default=dt.datetime.utcnow)

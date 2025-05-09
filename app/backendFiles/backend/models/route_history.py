from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, JSON
from database import Base
from datetime import datetime

class RouteHistory(Base):
    __tablename__ = "route_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    route_taken = Column(JSON, nullable=False)  # Store as list of lat-lng or GeoJSON
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    status = Column(String, default="Safe")  # Can be "Safe", "Alert triggered", etc.

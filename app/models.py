from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)
    device_id = Column(String, nullable=True)
    event_type = Column(String, index=True)
    timestamp = Column(DateTime, server_default=func.now())
    barcode = Column(Integer, nullable=True)
    points = Column(Integer)


class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    device_id = Column(String, nullable=True, index=True)
    badge_name = Column(String)
    level = Column(Integer, default=1)

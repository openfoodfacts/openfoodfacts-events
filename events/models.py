import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime

from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    device_id = Column(String, nullable=True)
    event_type = Column(String)
    timestamp = Column(DateTime)
    barcode = Column(Integer, nullable=True)

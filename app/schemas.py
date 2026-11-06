from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_type: str
    timestamp: Optional[datetime] = None
    user_id: Optional[str] = None
    barcode: Optional[str] = None
    points: Optional[int] = None


class EventCreate(EventBase):
    device_id: Optional[str] = None


class BadgeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: Optional[str] = None
    badge_name: str
    level: int

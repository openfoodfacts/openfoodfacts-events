from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_type: str
    timestamp: Optional[datetime]
    user_id: Optional[str]
    barcode: Optional[str]
    points: Optional[int]

class EventCreate(EventBase):
    device_id: Optional[str]


class BadgeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: Optional[str]
    badge_name: str
    level: int

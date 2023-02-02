from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    event_type: str
    timestamp: Optional[datetime]
    user_id: Optional[str]
    barcode: Optional[int]
    points: Optional[int]

    class Config:
        orm_mode = True


class EventCreate(EventBase):
    device_id: Optional[str]


class BadgeBase(BaseModel):
    user_id: Optional[str]
    badge_name: str
    level: int

    class Config:
        orm_mode = True

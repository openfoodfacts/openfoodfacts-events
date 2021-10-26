from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Event(BaseModel):
    event_type: str
    timestamp: datetime = datetime.utcnow()
    user_id: Optional[str]
    device_id: Optional[str]
    barcode: Optional[str]

    class Config:
        orm_mode = True

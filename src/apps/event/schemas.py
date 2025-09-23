from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class EventSchema(BaseModel):
    host_id: Optional[str]
    title: Optional[str] = Field(None, max_length=155)
    description: Optional[str] = None
    time: Optional[List[datetime]] = []
    banner_id: Optional[str] = None
    gallery: Optional[List[str]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = Field(None, max_length=500)
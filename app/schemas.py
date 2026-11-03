from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# response models (us -> user), how we want to structure the data that we send back

class Mosque(BaseModel):
    name: str
    google_places_id: str
    address: str
    rating: Optional[float] = None

    class Config:
        orm_mode = True

class Review(BaseModel):
    author: Optional[str] = None
    rating: Optional[float] = None
    review_text: Optional[str] = None
    review_date: Optional[datetime] = None

    class Config:
        orm_mode = True

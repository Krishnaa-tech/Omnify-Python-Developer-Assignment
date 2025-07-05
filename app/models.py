from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class ClassBase(BaseModel):
    name: str
    date: str # YYYY-MM-DD
    time: str # HH:MM
    instructor: str
    timezone: str # e.g., "Asia/Kolkata"

class ClassInDB(ClassBase):
    id: str
    total_slots: int
    available_slots: int

class ClassResponse(ClassInDB):
    # This model can be used for GET /classes, possibly with converted time
    display_date: str = Field(..., description="Date of the class in the requested timezone")
    display_time: str = Field(..., description="Time of the class in the requested timezone")

class BookingRequest(BaseModel):
    class_id: str = Field(..., description="ID of the class to book")
    client_name: str = Field(..., min_length=2, max_length=100)
    client_email: EmailStr

class BookingInDB(BaseModel):
    booking_id: str
    class_id: str
    client_name: str
    client_email: EmailStr
    booking_time: datetime # UTC datetime when booking was made

class BookingResponse(BookingInDB):
    # Potentially include class details for the /bookings endpoint
    class_name: Optional[str] = None
    class_date: Optional[str] = None
    class_time: Optional[str] = None
    class_instructor: Optional[str] = None
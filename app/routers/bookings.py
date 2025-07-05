from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from ..data import CLASSES, BOOKINGS, get_next_booking_id
from ..models import BookingRequest, BookingInDB, BookingResponse, ClassInDB
from datetime import datetime
from pydantic import EmailStr
import pytz
import re

router = APIRouter()

def _find_class_by_id(class_id: str) -> Optional[dict]:
    """Helper to find a class by its ID."""
    for cls in CLASSES:
        if cls["id"] == class_id:
            return cls
    return None

def _validate_email(email: str) -> bool:
    """Basic email format validation."""
    # This is a very basic regex, consider more robust solutions for production
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(regex, email) is not None

@router.post("/book", response_model=BookingResponse, status_code=status.HTTP_201_CREATED, summary="Book a spot in a fitness class")
async def book_class(booking_request: BookingRequest):
    """
    Accepts a booking request for a fitness class.
    Validates slot availability and processes the booking.
    """
    class_id = booking_request.class_id
    client_name = booking_request.client_name
    client_email = booking_request.client_email

    # 1. Input Validation (Pydantic handles most, but specific checks here)
    if not client_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client name cannot be empty."
        )
    if not _validate_email(client_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client email format."
        )

    # 2. Find the class
    class_obj = _find_class_by_id(class_id)
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with ID '{class_id}' not found."
        )

    # 3. Check for available slots
    if class_obj["available_slots"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # Conflict indicates resource state prevents action
            detail=f"No slots available for class '{class_obj['name']}'."
        )

    # 4. Check if the class is in the past
    current_time_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
    class_datetime_str = f"{class_obj['date']} {class_obj['time']}"
    try:
        class_dt_naive = datetime.strptime(class_datetime_str, "%Y-%m-%d %H:%M")
        class_dt_aware_ist = pytz.timezone("Asia/Kolkata").localize(class_dt_naive)
        
        if class_dt_aware_ist < current_time_ist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot book class '{class_obj['name']}' as it is in the past."
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error: Invalid class date/time format."
        )

    # 5. Process Booking
    class_obj["available_slots"] -= 1 # Decrement available slots

    booking_id = get_next_booking_id()
    new_booking = BookingInDB(
        booking_id=booking_id,
        class_id=class_id,
        client_name=client_name,
        client_email=client_email,
        booking_time=datetime.now(pytz.utc) # Store booking time in UTC
    )
    BOOKINGS.append(new_booking.dict()) # Store as dict for simplicity with in-memory list

    return BookingResponse(
        booking_id=new_booking.booking_id,
        class_id=new_booking.class_id,
        client_name=new_booking.client_name,
        client_email=new_booking.client_email,
        booking_time=new_booking.booking_time,
        class_name=class_obj['name'],
        class_date=class_obj['date'],
        class_time=class_obj['time'],
        class_instructor=class_obj['instructor']
    )

@router.get("/bookings", response_model=List[BookingResponse], summary="Get all bookings by a client email")
async def get_bookings_by_email(client_email: EmailStr = Query(..., description="Email address of the client")):
    """
    Returns all bookings made by a specific email address.
    """
    if not _validate_email(client_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client email format."
        )

    client_bookings = []
    for booking_data in BOOKINGS:
        if booking_data["client_email"].lower() == client_email.lower():
            # Enrich booking data with class details
            class_obj = _find_class_by_id(booking_data["class_id"])
            
            booking_response = BookingResponse(
                booking_id=booking_data['booking_id'],
                class_id=booking_data['class_id'],
                client_name=booking_data['client_name'],
                client_email=booking_data['client_email'],
                booking_time=booking_data['booking_time']
            )
            
            if class_obj:
                booking_response.class_name = class_obj['name']
                booking_response.class_date = class_obj['date']
                booking_response.class_time = class_obj['time']
                booking_response.class_instructor = class_obj['instructor']
            
            client_bookings.append(booking_response)
            
    return client_bookings
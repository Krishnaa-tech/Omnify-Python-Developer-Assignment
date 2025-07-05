from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from ..data import CLASSES
from ..models import ClassResponse
from ..utils.timezone_utils import convert_datetime_to_target_timezone
from datetime import datetime
import pytz

router = APIRouter()

@router.get("/classes", response_model=List[ClassResponse], summary="Get all upcoming fitness classes")
async def get_classes(
    target_timezone: Optional[str] = Query(None, description="Optional timezone to convert class times to (e.g., 'America/New_York'). If not provided, times will be in IST.")
):
    """
    Returns a list of all upcoming fitness classes.
    Optionally converts class times to a specified timezone.
    """
    current_time_ist = datetime.now(pytz.timezone("Asia/Kolkata"))
    upcoming_classes = []

    for cls in CLASSES:
        # Check if the class is in the future
        class_datetime_str = f"{cls['date']} {cls['time']}"
        try:
            class_dt_naive = datetime.strptime(class_datetime_str, "%Y-%m-%d %H:%M")
            class_dt_aware_ist = pytz.timezone("Asia/Kolkata").localize(class_dt_naive)
            
            if class_dt_aware_ist < current_time_ist:
                continue # Skip past classes
        except ValueError:
            # Handle cases where date/time format in data might be wrong
            print(f"Warning: Invalid date/time format for class ID {cls['id']}: {class_datetime_str}")
            continue

        display_date = cls['date']
        display_time = cls['time']

        if target_timezone:
            display_date, display_time = convert_datetime_to_target_timezone(
                cls['date'],
                cls['time'],
                cls['timezone'], # Source timezone is always IST as per requirement
                target_timezone
            )

        upcoming_classes.append(
            ClassResponse(
                id=cls['id'],
                name=cls['name'],
                date=cls['date'], # Original stored date/time
                time=cls['time'],
                instructor=cls['instructor'],
                total_slots=cls['total_slots'],
                available_slots=cls['available_slots'],
                timezone=cls['timezone'],
                display_date=display_date,
                display_time=display_time
            )
        )
    return upcoming_classes
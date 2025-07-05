from datetime import datetime
import pytz

# Seed data for classes
# Storing times as strings in IST for simplicity, will be parsed/converted as needed
CLASSES = [
    {
        "id": "yoga_001",
        "name": "Morning Yoga Flow",
        "date": "2025-07-06", # Tomorrow
        "time": "07:00",
        "instructor": "Priya Sharma",
        "total_slots": 10,
        "available_slots": 10,
        "timezone": "Asia/Kolkata"
    },
    {
        "id": "zumba_001",
        "name": "High-Energy Zumba",
        "date": "2025-07-06",
        "time": "18:30",
        "instructor": "Amit Singh",
        "total_slots": 15,
        "available_slots": 15,
        "timezone": "Asia/Kolkata"
    },
    {
        "id": "hiit_001",
        "name": "HIIT Blast",
        "date": "2025-07-07",
        "time": "09:00",
        "instructor": "Rajesh Kumar",
        "total_slots": 8,
        "available_slots": 8,
        "timezone": "Asia/Kolkata"
    },
    {
        "id": "yoga_002",
        "name": "Evening Restorative Yoga",
        "date": "2025-07-07",
        "time": "19:00",
        "instructor": "Priya Sharma",
        "total_slots": 12,
        "available_slots": 12,
        "timezone": "Asia/Kolkata"
    }
]

# In-memory storage for bookings
BOOKINGS = []

# For generating unique IDs (simple increment for demo)
_booking_id_counter = 0

def get_next_booking_id():
    global _booking_id_counter
    _booking_id_counter += 1
    return f"book_{_booking_id_counter:03d}"
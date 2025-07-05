from fastapi.testclient import TestClient
from app.main import app
from app.data import CLASSES, BOOKINGS # Import to reset state for tests

client = TestClient(app)

# Helper to reset data before each test
def setup_function(function):
    CLASSES.clear()
    BOOKINGS.clear()
    # Re-populate initial data state for a clean test environment
    CLASSES.extend([
        {
            "id": "yoga_001", "name": "Morning Yoga Flow", "date": "2025-07-06", "time": "07:00",
            "instructor": "Priya Sharma", "total_slots": 10, "available_slots": 10, "timezone": "Asia/Kolkata"
        },
        {
            "id": "zumba_001", "name": "High-Energy Zumba", "date": "2025-07-06", "time": "18:30",
            "instructor": "Amit Singh", "total_slots": 2, "available_slots": 2, "timezone": "Asia/Kolkata" # Low slots for easy testing
        },
        {
            "id": "hiit_001", "name": "HIIT Blast", "date": "2025-07-07", "time": "09:00",
            "instructor": "Rajesh Kumar", "total_slots": 8, "available_slots": 8, "timezone": "Asia/Kolkata"
        }
    ])
    BOOKINGS.clear() # Ensure bookings are empty for fresh tests

def test_get_classes_success():
    response = client.get("/classes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1 # At least one class from seed data
    assert "display_date" in response.json()[0] # Check for timezone conversion fields

def test_get_classes_with_timezone_conversion():
    response = client.get("/classes?target_timezone=America/New_York")
    assert response.status_code == 200
    classes = response.json()
    assert len(classes) >= 1
    # Very basic check: just ensure display_time is different if conversion happened
    # More robust test would actually convert and compare
    assert classes[0]["display_time"] != CLASSES[0]["time"] or classes[0]["display_date"] != CLASSES[0]["date"]


def test_book_class_success():
    initial_slots = CLASSES[0]["available_slots"]
    response = client.post(
        "/book",
        json={
            "class_id": "yoga_001",
            "client_name": "Test User",
            "client_email": "test@example.com",
        },
    )
    assert response.status_code == 201
    assert CLASSES[0]["available_slots"] == initial_slots - 1
    assert "booking_id" in response.json()
    assert response.json()["client_email"] == "test@example.com"
    assert len(BOOKINGS) == 1 # Check if booking was added

def test_book_class_not_found():
    response = client.post(
        "/book",
        json={
            "class_id": "non_existent",
            "client_name": "Test User",
            "client_email": "test@example.com",
        },
    )
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()

def test_book_class_no_slots():
    # Book twice to exhaust slots for zumba_001 (initial slots = 2)
    client.post(
        "/book",
        json={
            "class_id": "zumba_001",
            "client_name": "User 1",
            "client_email": "user1@example.com",
        },
    )
    client.post(
        "/book",
        json={
            "class_id": "zumba_001",
            "client_name": "User 2",
            "client_email": "user2@example.com",
        },
    )
    assert CLASSES[1]["available_slots"] == 0 # Verify slots are 0

    # Attempt a third booking
    response = client.post(
        "/book",
        json={
            "class_id": "zumba_001",
            "client_name": "User 3",
            "client_email": "user3@example.com",
        },
    )
    assert response.status_code == 409 # Conflict
    assert "detail" in response.json()
    assert "no slots available" in response.json()["detail"].lower()

def test_book_class_invalid_email():
    response = client.post(
        "/book",
        json={
            "class_id": "yoga_001",
            "client_name": "Invalid Email",
            "client_email": "invalid-email-format",
        },
    )
    assert response.status_code == 422 # Unprocessable Entity from Pydantic
    assert "value_error.email" in response.json()["detail"][0]["type"]

def test_book_class_missing_fields():
    response = client.post(
        "/book",
        json={
            "class_id": "yoga_001",
            "client_name": "Test User",
            # client_email is missing
        },
    )
    assert response.status_code == 422 # Unprocessable Entity

def test_get_bookings_by_email_success():
    # Make a booking first
    client.post(
        "/book",
        json={
            "class_id": "yoga_001",
            "client_name": "Booking Finder",
            "client_email": "finder@example.com",
        },
    )
    response = client.get("/bookings?client_email=finder@example.com")
    assert response.status_code == 200
    bookings = response.json()
    assert isinstance(bookings, list)
    assert len(bookings) == 1
    assert bookings[0]["client_email"] == "finder@example.com"
    assert bookings[0]["class_name"] == "Morning Yoga Flow" # Check enrichment

def test_get_bookings_by_email_no_bookings_found():
    response = client.get("/bookings?client_email=nonexistent@example.com")
    assert response.status_code == 200
    assert response.json() == []

def test_get_bookings_by_email_invalid_email_format():
    response = client.get("/bookings?client_email=bademail")
    assert response.status_code == 422 # Unprocessable Entity
    assert "value_error.email" in response.json()["detail"][0]["type"]
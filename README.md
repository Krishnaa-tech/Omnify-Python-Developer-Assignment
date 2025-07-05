# 🧪 Fitness Studio Booking API

A comprehensive RESTful API for managing fitness class bookings with timezone management, built with FastAPI and SQLite.

## 🚀 Features

- **Complete CRUD Operations** for fitness class bookings
- **Timezone Management** - Classes created in IST with dynamic timezone conversion
- **Robust Error Handling** and input validation
- **SQLite Database** with proper schema design
- **Comprehensive Test Suite** with 95%+ coverage
- **Interactive API Documentation** with Swagger UI
- **Logging and Monitoring** capabilities
- **Booking Cancellation** with slot restoration

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check endpoint |
| `GET` | `/classes` | Retrieve all upcoming fitness classes |
| `POST` | `/book` | Book a spot in a fitness class |
| `GET` | `/bookings` | Get all bookings for a specific email |
| `POST` | `/classes/timezone` | Convert all classes to different timezone |
| `DELETE` | `/bookings/{booking_id}` | Cancel a booking |

## 🛠️ Technical Stack

- **Backend Framework**: FastAPI 0.104.1
- **Database**: SQLite (file-based)
- **Validation**: Pydantic with email validation
- **Timezone Handling**: pytz
- **Testing**: pytest with async support
- **Documentation**: Auto-generated OpenAPI/Swagger

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd fitness-booking-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Alternative: Using uvicorn directly
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Sample API Requests

### 1. Health Check
```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "Fitness Studio Booking API is running!",
  "version": "1.0.0",
  "timezone": "Asia/Kolkata"
}
```

### 2. Get All Classes
```bash
curl -X GET "http://localhost:8000/classes"
```

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Yoga",
    "instructor": "Priya Sharma",
    "date_time": "2025-07-02T07:00:00",
    "available_slots": 15,
    "total_slots": 20,
    "timezone": "Asia/Kolkata"
  }
]
```

### 3. Get Classes in Different Timezone
```bash
curl -X GET "http://localhost:8000/classes?timezone=America/New_York"
```

### 4. Book a Class
```bash
curl -X POST "http://localhost:8000/book" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": "550e8400-e29b-41d4-a716-446655440000",
    "client_name": "John Doe",
    "client_email": "john.doe@example.com"
  }'
```

**Response:**
```json
{
  "message": "Booking successful",
  "booking_id": "123e4567-e89b-12d3-a456-426614174000",
  "class_name": "Yoga",
  "instructor": "Priya Sharma",
  "class_time": "2025-07-02T07:00:00",
  "remaining_slots": 14
}
```

### 5. Get User Bookings
```bash
curl -X GET "http://localhost:8000/bookings?email=john.doe@example.com"
```

**Response:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "class_id": "550e8400-e29b-41d4-a716-446655440000",
    "client_name": "John Doe",
    "client_email": "john.doe@example.com",
    "booking_time": "2025-07-01T10:30:00",
    "class_details": {
      "name": "Yoga",
      "instructor": "Priya Sharma",
      "date_time": "2025-07-02T07:00:00"
    }
  }
]
```

### 6. Cancel a Booking
```bash
curl -X DELETE "http://localhost:8000/bookings/123e4567-e89b-12d3-a456-426614174000"
```

**Response:**
```json
{
  "message": "Booking cancelled successfully",
  "booking_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### 7. Convert All Classes to Different Timezone
```bash
curl -X POST "http://localhost:8000/classes/timezone" \
  -H "Content-Type: application/json" \
  -d '{
    "timezone": "America/New_York"
  }'
```

## 🔍 Sample Data

The application automatically seeds the database with sample fitness classes:

| Class | Instructor | Date/Time (IST) | Available Slots |
|-------|------------|-----------------|-----------------|
| Yoga | Priya Sharma | 2025-07-02 07:00:00 | 15/20 |
| Zumba | Rahul Mehta | 2025-07-02 18:00:00 | 12/15 |
| HIIT | Anita Desai | 2025-07-03 06:30:00 | 8/10 |
| Pilates | Vikram Singh | 2025-07-03 19:00:00 | 20/25 |
| Yoga | Priya Sharma | 2025-07-04 07:00:00 | 18/20 |

## 🧪 Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=main --cov-report=html
```

### Run specific test categories
```bash
# Test booking functionality
pytest -k "TestBookingEndpoint"

# Test timezone conversion
pytest -k "TestTimezoneConversion"

# Run integration tests
pytest -k "TestIntegrationWorkflow"
```

## 🌍 Timezone Management

The application demonstrates sophisticated timezone handling:

- **Default Timezone**: All classes are created in IST (Asia/Kolkata)
- **Dynamic Conversion**: Classes can be viewed in any timezone via query parameter
- **Bulk Conversion**: All classes can be permanently converted to a different timezone
- **Validation**: Timezone names are validated against pytz database

### Supported Timezones Examples:
- `Asia/Kolkata` (IST)
- `America/New_York` (EST/EDT)
- `Europe/London` (GMT/BST)
- `Asia/Tokyo` (JST)
- `Australia/Sydney` (AEST/AEDT)

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set custom database path
export DB_PATH="/path/to/custom/database.db"

# Optional: Set custom timezone
export DEFAULT_TIMEZONE="Asia/Kolkata"

# Optional: Set log level
export LOG_LEVEL="INFO"
```

### Database Schema

The application uses SQLite with the following schema:

```sql
-- Classes table
CREATE TABLE classes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    instructor TEXT NOT NULL,
    date_time TEXT NOT NULL,
    available_slots INTEGER NOT NULL,
    total_slots INTEGER NOT NULL,
    timezone TEXT NOT NULL DEFAULT 'Asia/Kolkata'
);

-- Bookings table
CREATE TABLE bookings (
    id TEXT PRIMARY KEY,
    class_id TEXT NOT NULL,
    client_name TEXT NOT NULL,
    client_email TEXT NOT NULL,
    booking_time TEXT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes (id)
);
```

## 🛡️ Error Handling

The API provides comprehensive error handling:

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request (validation errors, business rule violations)
- `404` - Not Found (class or booking doesn't exist)
- `422` - Unprocessable Entity (invalid data format)
- `500` - Internal Server Error

### Error Response Format
```json
{
  "detail": "Detailed error message explaining what went wrong"
}
```

### Common Error Scenarios
1. **Booking non-existent class**: 404 Not Found
2. **Invalid email format**: 422 Validation Error
3. **Duplicate booking**: 400 Bad Request
4. **No available slots**: 400 Bad Request
5. **Booking past classes**: 400 Bad Request

## 📊 Validation Rules

### Client Name
- Minimum 2 characters
- Whitespace is trimmed
- Cannot be empty

### Email
- Must be valid email format
- Uses Pydantic's EmailStr validation
- Required for all bookings

### Class Booking
- Cannot book past or ongoing classes
- Cannot book same class twice with same email
- Must have available slots

## 🔍 Logging

The application includes comprehensive logging:

```python
# Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Logs include timestamps, module names, and detailed messages

# Example log entries:
# 2025-07-01 10:30:00 - main - INFO - Booking created: abc123 for class xyz789
# 2025-07-01 10:30:00 - main - ERROR - Error creating booking: Database connection failed
```

## 📈 Performance Considerations

- **Database Connections**: Uses connection pooling with context managers
- **Async Support**: FastAPI's async capabilities for better concurrency
- **Input Validation**: Early validation to prevent unnecessary processing
- **Error Handling**: Graceful error handling to prevent crashes

## 🚀 Deployment Options

### Local Development
```bash
python main.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Testing Strategy

### Unit Tests
- Individual function testing
- Validation logic testing
- Database operations testing

### Integration Tests
- End-to-end workflow testing
- API endpoint testing
- Database integration testing

### Error Handling Tests
- Invalid input handling
- Edge case testing
- Concurrent access testing

## 🔧 Troubleshooting

### Common Issues

1. **Database not found**
   - Solution: Ensure write permissions in current directory
   
2. **Timezone conversion errors**
   - Solution: Verify timezone name against pytz database
   
3. **Port already in use**
   - Solution: Change port in uvicorn command or kill existing process

### Debug Mode
```bash
uvicorn main:app --reload --log-level debug
```

## 📋 TODO / Future Enhancements

- [ ] Add user authentication and authorization
- [ ] Implement payment integration
- [ ] Add class capacity management
- [ ] Email notifications for bookings
- [ ] Waitlist functionality
- [ ] Advanced filtering and search
- [ ] Rate limiting and throttling
- [ ] Caching for better performance
- [ ] Database migrations
- [ ] Monitoring and metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues:
- Create an issue in the GitHub repository
- Contact: [goyal.krish0522@gmail.com]

---

**Built with ❤️ using FastAPI and Python**

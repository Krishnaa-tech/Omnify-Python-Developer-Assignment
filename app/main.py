from fastapi import FastAPI
from .routers import classes, bookings
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fitness Studio Booking API",
    description="A simple API for viewing and booking fitness classes.",
    version="1.0.0"
)

# Include routers
app.include_router(classes.router, tags=["Classes"])
app.include_router(bookings.router, tags=["Bookings"])

@app.get("/", include_in_schema=False)
async def read_root():
    """Root endpoint to show API is running."""
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the Fitness Studio Booking API. Go to /docs for API documentation."}
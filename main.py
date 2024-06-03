from fastapi import FastAPI
from route.api import api_router

# Create FastAPI instance
app = FastAPI()

# Include API routers
app.include_router(api_router)

# Run migrations
# If you're using Alembic for database migrations, you might run them here

if __name__ == "__main__":
    # Run the application
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

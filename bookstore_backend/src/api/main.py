from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.books import router as books_router

# Initialize FastAPI app with metadata and tags
app = FastAPI(
    title="Bookstore Backend API",
    description="APIs for the Bookstore application including book catalog browsing.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Books", "description": "Endpoints for browsing and retrieving books"},
        {"name": "Health", "description": "Service health and status"},
    ],
)

# Configure CORS to allow the frontend at http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(books_router)

@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Simple health check endpoint used for uptime checks."""
    return {"message": "Healthy"}

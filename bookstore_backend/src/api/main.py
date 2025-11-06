from os import getenv
from urllib.parse import urlparse

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

# Derive allowed CORS origins:
# - Local dev ports
# - Preview environment base for port 3000 (same host as backend but port 3000)
# - Optional REACT_APP_FRONTEND_URL from env if provided
frontend_env = getenv("REACT_APP_FRONTEND_URL")
backend_url = getenv("REACT_APP_BACKEND_URL") or getenv("REACT_APP_API_BASE")
allowed_origins = {
    "http://localhost:3000",
    "http://127.0.0.1:3000",
}

# Add preview origin by rewriting current backend host to port 3000
if backend_url:
    try:
        parsed = urlparse(backend_url)
        if parsed.scheme and parsed.hostname:
            preview_origin = f"{parsed.scheme}://{parsed.hostname}:3000"
            allowed_origins.add(preview_origin)
    except Exception:
        # If parsing fails, we silently ignore and keep defaults
        pass

# Add env-provided frontend origin if present
if frontend_env:
    allowed_origins.add(frontend_env)

# Configure CORS to allow the frontend and common methods/headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (books router already includes '/api/books' prefix)
app.include_router(books_router)

@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Simple health check endpoint used for uptime checks."""
    return {"message": "Healthy"}

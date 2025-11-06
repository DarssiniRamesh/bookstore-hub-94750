from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

# Seeded in-memory data store for books. In a real app, this would be a database.
_SEEDED_BOOKS = [
    {
        "id": 1,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "description": "A comprehensive guide for software developers on practical approaches and best practices.",
        "price": 39.99,
        "rating": 4.8,
        "image_url": "https://images-na.ssl-images-amazon.com/images/I/41as+WafrFL._SX258_BO1,204,203,200_.jpg",
        "category": "Software",
    },
    {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "description": "A Handbook of Agile Software Craftsmanship, focusing on writing clean, maintainable code.",
        "price": 34.95,
        "rating": 4.7,
        "image_url": "https://images-na.ssl-images-amazon.com/images/I/41xShlnTZTL._SX374_BO1,204,203,200_.jpg",
        "category": "Software",
    },
    {
        "id": 3,
        "title": "Atomic Habits",
        "author": "James Clear",
        "description": "An Easy & Proven Way to Build Good Habits & Break Bad Ones.",
        "price": 21.99,
        "rating": 4.8,
        "image_url": "https://images-na.ssl-images-amazon.com/images/I/51-uspgqWIL._SX329_BO1,204,203,200_.jpg",
        "category": "Self-Help",
    },
    {
        "id": 4,
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "description": "A novel about all the choices that go into a life well lived.",
        "price": 16.99,
        "rating": 4.3,
        "image_url": "https://images-na.ssl-images-amazon.com/images/I/41s+uO1tZgL._SX329_BO1,204,203,200_.jpg",
        "category": "Fiction",
    },
]


class BookBase(BaseModel):
    """Base fields shared by book responses."""
    id: int = Field(..., description="Unique identifier of the book")
    title: str = Field(..., description="Title of the book")
    author: str = Field(..., description="Author of the book")
    price: float = Field(..., description="Price of the book in USD")
    rating: float = Field(..., ge=0, le=5, description="Average rating out of 5")
    image_url: str = Field(..., description="URL to the cover image")
    category: str = Field(..., description="Category or genre of the book")


class Book(BookBase):
    """Full book model including description."""
    description: str = Field(..., description="Detailed description or synopsis of the book")


class BookListResponse(BaseModel):
    """Paginated list response for books."""
    total: int = Field(..., description="Total number of books matching the filter")
    limit: int = Field(..., description="Requested page size")
    offset: int = Field(..., description="Requested offset")
    items: List[BookBase] = Field(..., description="Books for the current page")


router = APIRouter(prefix="/api/books", tags=["Books"])

# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=BookListResponse,
    summary="List books",
    description="Returns a paginated list of books. Supports optional filtering by category.",
    responses={
        200: {"description": "List of books returned successfully"},
    },
)
def list_books(
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip before starting to collect the result set"),
    category: Optional[str] = Query(None, description="Filter books by category"),
) -> BookListResponse:
    """List books with optional category filter and pagination."""
    # Filter by category if provided (case-insensitive)
    filtered = _SEEDED_BOOKS
    if category:
        filtered = [b for b in _SEEDED_BOOKS if b["category"].lower() == category.lower()]

    total = len(filtered)
    # Pagination slice
    page_items = filtered[offset : offset + limit]
    # Return summary model (without description field)
    summary_items = [
        BookBase(
            id=item["id"],
            title=item["title"],
            author=item["author"],
            price=item["price"],
            rating=item["rating"],
            image_url=item["image_url"],
            category=item["category"],
        )
        for item in page_items
    ]
    return BookListResponse(total=total, limit=limit, offset=offset, items=summary_items)


# PUBLIC_INTERFACE
@router.get(
    "/{book_id}",
    response_model=Book,
    summary="Get book details",
    description="Returns the full details for a single book by its ID.",
    responses={
        200: {"description": "Book details returned successfully"},
        404: {"description": "Book not found"},
    },
)
def get_book(book_id: int) -> Book:
    """Get full details of a single book by id or raise 404."""
    for item in _SEEDED_BOOKS:
        if item["id"] == book_id:
            return Book(**item)
    raise HTTPException(status_code=404, detail="Book not found")

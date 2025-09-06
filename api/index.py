from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
from fastapi.templating import Jinja2Templates
import logging
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS policy for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2 Templates (used for the homepage)
import os
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=template_dir)

# Google API Key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.error("Missing Google API key. Set GOOGLE_API_KEY as environment variable.")
    raise RuntimeError("Missing GOOGLE_API_KEY")

class Restaurant(BaseModel):
    name: str
    rating: float
    cuisine: Optional[str] = None
    price_level: Optional[int] = None
    address: str
    place_id: str

def get_restaurants_from_google(location: str) -> List[Restaurant]:
    logger.info(f"Fetching restaurants from Google Places for: {location}")
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"restaurants in {location}",
        "key": GOOGLE_API_KEY,
        "type": "restaurant"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Google API request failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch restaurants")

    results = response.json().get("results", [])
    if not results:
        logger.warning(f"No restaurants found for location: {location}")
        return []

    restaurants_list = [
        Restaurant(
            name=r["name"],
            rating=float(r.get("rating", 0.0)),
            price_level=r.get("price_level"),
            address=r.get("formatted_address"),
            place_id=r["place_id"]
        ) for r in results
    ]

    return restaurants_list

@app.get("/")
def index(request: Request):
    try:
        logger.info("Serving homepage template")
        return templates.TemplateResponse(
            name="index.html",
            context={"request": request}
        )
    except Exception as e:
        logger.error(f"Template error: {e}")
        # Fallback to simple HTML response
        return {
            "message": "Restaurant Finder API is working!",
            "endpoints": {
                "home": "/",
                "restaurants": "/restaurants/{location}",
                "example": "/restaurants/New York"
            },
            "template_error": str(e)
        }

@app.get("/restaurants/{location}", response_model=List[Restaurant])
async def get_all_restaurants(
    location: str,
    min_rating: float = Query(0.0, ge=0.0, le=5.0),
    max_price: Optional[int] = Query(None, ge=0, le=4),
    limit: int = Query(10, ge=1)
):
    raw_restaurants = get_restaurants_from_google(location)

    # Apply filters
    filtered = [
        r for r in raw_restaurants
        if r.rating >= min_rating and (max_price is None or (r.price_level is not None and r.price_level <= max_price))
    ]

    # Sort by rating descending
    sorted_restaurants = sorted(filtered, key=lambda x: x.rating, reverse=True)

    return sorted_restaurants[:limit]

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is working"}

# This is the handler for Vercel
from mangum import Mangum

handler = Mangum(app)

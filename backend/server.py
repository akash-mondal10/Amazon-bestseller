from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
import sys

# Add amazon_analyzer to path
sys.path.insert(0, str(Path(__file__).parent / 'amazon_analyzer' / 'src'))

from data_loader import DataLoader
from preprocessing import DataPreprocessor
from analysis import DataAnalyzer

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Initialize data once at startup
print("Loading and preprocessing Amazon Bestsellers dataset...")
loader = DataLoader()
df = loader.load_data()
preprocessor = DataPreprocessor(df)
preprocessor.check_duplicates()
preprocessor.remove_duplicates()
preprocessor.validate_data_types()
clean_df = preprocessor.get_clean_data()
analyzer = DataAnalyzer(clean_df)
print(f"Dataset ready: {len(clean_df)} books loaded")

# Create the main app
app = FastAPI(title="Amazon Bestseller Analyzer API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Response Models
class SummaryStats(BaseModel):
    total_books: int
    avg_rating: float
    avg_price: float
    total_reviews: int
    genres: List[str]
    year_range: List[int]


class TopAuthors(BaseModel):
    authors: List[str]
    counts: List[int]


class GenreDistribution(BaseModel):
    genres: List[str]
    counts: List[int]
    percentages: List[float]


class YearTrends(BaseModel):
    years: List[int]
    book_counts: List[int]
    avg_ratings: List[float]
    avg_prices: List[float]
    avg_reviews: List[int]


class PriceRatingData(BaseModel):
    prices: List[float]
    ratings: List[float]
    names: List[str]
    genres: List[str]
    correlation: float


class CorrelationMatrix(BaseModel):
    columns: List[str]
    matrix: List[List[float]]


class Book(BaseModel):
    Name: str
    Author: str
    User_Rating: float
    Reviews: int
    Price: float
    Year: int
    Genre: str


class FilterOptions(BaseModel):
    years: List[int]
    genres: List[str]


# API Endpoints
@api_router.get("/")
async def root():
    return {
        "message": "Amazon Bestseller Analyzer API",
        "version": "1.0",
        "endpoints": [
            "/api/summary",
            "/api/top-authors",
            "/api/genre-distribution",
            "/api/year-trends",
            "/api/price-rating",
            "/api/correlation",
            "/api/books",
            "/api/insights",
            "/api/filter-options"
        ]
    }


@api_router.get("/summary", response_model=SummaryStats)
async def get_summary():
    """Get summary statistics of the dataset."""
    return {
        "total_books": len(clean_df),
        "avg_rating": float(clean_df['User Rating'].mean()),
        "avg_price": float(clean_df['Price'].mean()),
        "total_reviews": int(clean_df['Reviews'].sum()),
        "genres": clean_df['Genre'].unique().tolist(),
        "year_range": [int(clean_df['Year'].min()), int(clean_df['Year'].max())]
    }


@api_router.get("/top-authors", response_model=TopAuthors)
async def get_top_authors(n: int = 10):
    """Get top N authors by book count."""
    result = analyzer.get_top_authors(n)
    return result


@api_router.get("/genre-distribution", response_model=GenreDistribution)
async def get_genre_distribution():
    """Get distribution of books by genre."""
    return analyzer.get_genre_distribution()


@api_router.get("/year-trends", response_model=YearTrends)
async def get_year_trends():
    """Get year-wise trends."""
    return analyzer.get_year_wise_trends()


@api_router.get("/price-rating", response_model=PriceRatingData)
async def get_price_rating():
    """Get price vs rating data."""
    price_rating = analyzer.get_price_rating_analysis()
    # Add genre information for coloring
    price_rating['genres'] = clean_df['Genre'].tolist()
    return price_rating


@api_router.get("/correlation", response_model=CorrelationMatrix)
async def get_correlation():
    """Get correlation matrix."""
    return analyzer.get_correlation_matrix()


@api_router.get("/books")
async def get_books(
    year: Optional[int] = None,
    genre: Optional[str] = None,
    limit: int = 100
):
    """Get filtered books data."""
    filtered_df = analyzer.get_filtered_data(year=year, genre=genre)
    
    # Convert to records and limit results
    books = filtered_df.head(limit).to_dict('records')
    
    return {
        "total": len(filtered_df),
        "showing": len(books),
        "books": books
    }


@api_router.get("/insights")
async def get_insights():
    """Get generated insights from the data."""
    insights = analyzer.generate_insights()
    return {"insights": insights}


@api_router.get("/filter-options", response_model=FilterOptions)
async def get_filter_options():
    """Get available filter options."""
    return {
        "years": sorted(clean_df['Year'].unique().tolist()),
        "genres": sorted(clean_df['Genre'].unique().tolist())
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

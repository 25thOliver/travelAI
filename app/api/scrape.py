from fastapi import APIRouter
from app.services.scrape_service import ScrapeService

router = APIRouter(prefix="/scrape", tags=["scrape"])
scrape_service = ScrapeService()

@router.post("/")
async def scrape():
    count = await scrape_service.scrape_and_store()
    return {"stored_records": count}
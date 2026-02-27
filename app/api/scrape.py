from fastapi import APIRouter, Depends
from app.services.scrape_service import ScrapeService
from app.dependencies.auth import require_api_key

router = APIRouter(prefix="/scrape", tags=["scrape"])
scrape_service = ScrapeService()

@router.post("/", dependencies=[Depends(require_api_key)])
async def scrape():
    count = await scrape_service.scrape()
    return {"stored_records": count}
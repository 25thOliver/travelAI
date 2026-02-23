import asyncio
from app.celery_app import celery_app
from app.scraping.destination_scraper import DestinationScraper
from app.db.session import AsyncSessionLocal
from app.repositories.destination_repository import DestinationRepository


@celery_app.task
def scrape_destinations():
    async def run():
        scraper = DestinationScraper()
        data = await scraper.scrape_destinantions()

        async with AsyncSessionLocal() as db:
            repo = DestinationRepository(db)
            for item in data:
                await repo.create(**item)

    asyncio.run(run())
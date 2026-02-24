from app.scraping.destination_scraper import DestinationScraper
from app.db.session import AsyncSessionLocal
from app.repositories.destination_repository import DestinationRepository


class ScrapeService:
    async def scrape_and_store(self) -> int:
        scraper = DestinationScraper()
        data = await scraper.scrape_destinations()

        count = 0

        async with AsyncSessionLocal() as db:
            repo = DestinationRepository(db)

            for item in data:
                await repo.create(**item)
                count += 1
        return count
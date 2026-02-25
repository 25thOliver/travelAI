from app.scraping.destination_scraper import DestinationScraper
from app.db.session import AsyncSessionLocal
from app.repositories.destination_repository import DestinationRepository
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


class ScrapeService:
    async def scrape_and_store(self) -> int:
        scraper = DestinationScraper()
        data = await scraper.scrape_destinations()

        embedding_Service = EmbeddingService()
        vector_service = VectorService()

        count = 0

        async with AsyncSessionLocal() as db:
            repo = DestinationRepository(db)

            for item in data:
                db_obj = await repo.create(**item)

                text_for_embeding = (
                    f"{item['title']} - {item['description']}"
                )

                vector = await embedding_Service.embed(text_for_embeding)

                vector_service.upsert(
                    id=db_obj.id,
                    vector=vector,
                    payload=item,
                )

                count += 1
                
        return count
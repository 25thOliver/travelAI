import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

TARGET_URLS = [
    # Magical Kenya
    "https://magicalkenya.com/destinations/nairobi-national-park/",
    "https://magicalkenya.com/destinations/maasai-mara/",
    "https://magicalkenya.com/destinations/amboseli-national-park/",
    "https://magicalkenya.com/destinations/lake-nakuru-national-park/",
    "https://magicalkenya.com/destinations/tsavo-east-national-park/",
    "https://magicalkenya.com/destinations/tsavo-west-national-park/",

    # KWS
    "https://www.kws.go.ke/content/nairobi-national-park",
    "https://www.kws.go.ke/content/amboseli-national-park",
]

def chunk_text(text: str, chunk_size: int = 350):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".jion(words[i:i + chunk_size])


class ScrapeService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    async def scrape(self):
        self.vector_service.create_collection()
        stored = 0

        async with httpx.AsyncClient(timeout=30.0) as client:
            for url in TARGET_URLS:
                try:
                    response = await client.get(url)
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Structured content first
                    main = soup.find("main")
                    article = soup.find("article")

                    if main:
                        text = main.get_text(separator= " ")
                    elif article:
                        text = article.get_text(separator= " ")
                    else:
                        paragraphs = soup.find_all("p")
                        text = " ".join(p.get_text() for p in paragraphs)

                    title = soup.title.string if soup.title else "Unknown"

                    for chunk in chunk_text(text):
                        vector = await self.embedding_service.embed(chunk)

                        payload = {
                            "title": title,
                            "source_url": url,
                            "location": "Kenya",
                            "type": "national_park",
                            "description": chunk,
                        }

                        self.vector_service.upsert(
                            id=stored,
                            vector=vector,
                            payload=payload,
                        )

                        stored += 1

                except Exception as e:
                    print(f"Error scraping {url}: {e}")

        return stored
# app/services/scrape_service.py

import asyncio
import httpx
from bs4 import BeautifulSoup

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

# Magical Kenya pages for authoritative tourism data
TARGET_URLS = [
    # National Parks
    ("https://magicalkenya.com/places-to-visit/national-parks/nairobi-national-park/", "Nairobi National Park", "Nairobi"),
    ("https://magicalkenya.com/places-to-visit/national-parks/maasai-mara-national-reserve/", "Maasai Mara", "Narok"),
    ("https://magicalkenya.com/places-to-visit/national-parks/amboseli-national-park/", "Amboseli National Park", "Kajiado"),
    ("https://magicalkenya.com/places-to-visit/national-parks/tsavo-east-national-park/", "Tsavo East National Park", "Taita-Taveta"),
    ("https://magicalkenya.com/places-to-visit/national-parks/tsavo-west-national-park/", "Tsavo West National Park", "Taita-Taveta"),
    ("https://magicalkenya.com/places-to-visit/national-parks/lake-nakuru-national-park/", "Lake Nakuru National Park", "Nakuru"),
    ("https://magicalkenya.com/places-to-visit/national-parks/aberdare-national-park/", "Aberdare National Park", "Nyeri"),
    ("https://magicalkenya.com/places-to-visit/national-parks/meru-national-park/", "Meru National Park", "Meru"),
    ("https://magicalkenya.com/places-to-visit/national-parks/hells-gate-national-park/", "Hell's Gate National Park", "Nakuru"),
    ("https://magicalkenya.com/places-to-visit/national-parks/samburu-national-reserve/", "Samburu National Reserve", "Samburu"),
    
    # Beaches & Coast
    ("https://magicalkenya.com/places-to-visit/beaches/diani-beach/", "Diani Beach", "Kwale"),
    ("https://magicalkenya.com/places-to-visit/beaches/watamu/", "Watamu Beach", "Kilifi"),
    ("https://magicalkenya.com/places-to-visit/beaches/lamu/", "Lamu Island", "Lamu"),
    
    # Conservancies
    ("https://magicalkenya.com/places-to-visit/conservancies/ol-pejeta-conservancy/", "Ol Pejeta Conservancy", "Laikipia"),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def chunk_text(text: str, chunk_size: int = 150):
    """Split text into chunks of ~chunk_size words."""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])


async def fetch_with_retry(client: httpx.AsyncClient, url: str, retries: int = 3) -> str | None:
    """Fetch a URL with up to `retries` attempts on failure."""
    for attempt in range(1, retries + 1):
        try:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  Attempt {attempt} failed for {url}: {e}")
            if attempt < retries:
                await asyncio.sleep(2 ** attempt)  # 2s, 4s, 8s backoff
    return None


def extract_text(soup: BeautifulSoup) -> str:
    # Attempt to find standard main content areas
    for selector in ["article", "main", ".post-content", ".entry-content"]:
        content = soup.select_one(selector)
        if content:
            # strip out common noisy elements
            for tag in content.select("nav, footer, .sidebar, script, style"):
                tag.decompose()
            return content.get_text(separator=" ", strip=True)

    paragraphs = soup.find_all("p")
    return " ".join(p.get_text() for p in paragraphs)


class ScrapeService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()

    async def scrape(self):
        self.vector_service.create_collection()
        stored = 0

        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            for url, title, location in TARGET_URLS:
                print(f"Scraping: {title} ...")
                html = await fetch_with_retry(client, url)

                if not html:
                    print(f"  Skipped {title} — all retries failed")
                    continue

                soup = BeautifulSoup(html, "html.parser")
                text = extract_text(soup)

                if not text.strip():
                    print(f"  Skipped {title} — no text extracted")
                    continue

                chunks = list(chunk_text(text))
                print(f"  {len(chunks)} chunks extracted")

                for chunk in chunks:
                    vector = await self.embedding_service.embed(chunk)

                    payload = {
                        "title": title,
                        "source": url,
                        "location": location,
                        "country": "Kenya",
                        "type": "destination",
                        "description": chunk,
                    }

                    self.vector_service.upsert(
                        id=stored,
                        vector=vector,
                        payload=payload,
                    )

                    stored += 1

        print(f"Total stored: {stored} chunks")
        return stored
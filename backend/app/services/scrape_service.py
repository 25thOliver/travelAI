# app/services/scrape_service.py

import asyncio
import httpx
from bs4 import BeautifulSoup

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

# Wikipedia pages are reliable, open, and content-rich
TARGET_URLS = [
    # National Parks
    ("https://en.wikipedia.org/wiki/Nairobi_National_Park",       "Nairobi National Park",    "Nairobi"),
    ("https://en.wikipedia.org/wiki/Maasai_Mara",                 "Maasai Mara",               "Narok"),
    ("https://en.wikipedia.org/wiki/Amboseli_National_Park",      "Amboseli National Park",    "Kajiado"),
    ("https://en.wikipedia.org/wiki/Tsavo_East_National_Park",    "Tsavo East National Park",  "Taita-Taveta"),
    ("https://en.wikipedia.org/wiki/Tsavo_West_National_Park",    "Tsavo West National Park",  "Taita-Taveta"),
    ("https://en.wikipedia.org/wiki/Lake_Nakuru_National_Park",   "Lake Nakuru National Park", "Nakuru"),
    ("https://en.wikipedia.org/wiki/Aberdare_National_Park",      "Aberdare National Park",    "Nyeri"),
    ("https://en.wikipedia.org/wiki/Meru_National_Park",          "Meru National Park",        "Meru"),
    ("https://en.wikipedia.org/wiki/Hell%27s_Gate_National_Park", "Hell's Gate National Park", "Nakuru"),
    ("https://en.wikipedia.org/wiki/Samburu_National_Reserve",    "Samburu National Reserve",  "Samburu"),
    # Beaches & Coast
    ("https://en.wikipedia.org/wiki/Diani_Beach",                 "Diani Beach",               "Kwale"),
    ("https://en.wikipedia.org/wiki/Lamu",                        "Lamu Island",               "Lamu"),
    # Conservancies
    ("https://en.wikipedia.org/wiki/Ol_Pejeta_Conservancy",       "Ol Pejeta Conservancy",     "Laikipia"),
    ("https://en.wikipedia.org/wiki/Mount_Kenya_National_Park",   "Mount Kenya National Park", "Nyeri"),
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
    """Extract clean text — Wikipedia-aware, falls back to paragraphs."""
    # Wikipedia main content
    content = soup.select_one("#mw-content-text .mw-parser-output")
    if content:
        # Remove tables, navboxes, references
        for tag in content.select("table, .navbox, .reflist, sup, .mw-editsection"):
            tag.decompose()
        return content.get_text(separator=" ", strip=True)

    # Generic fallback
    for tag in soup.select("main, article"):
        return tag.get_text(separator=" ", strip=True)

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
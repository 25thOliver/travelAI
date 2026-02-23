import httpx
from bs4 import BeautifulSoup

class BaseScraper:
    async def fetch(self, url: str) -> str:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        
    def parse_html(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")
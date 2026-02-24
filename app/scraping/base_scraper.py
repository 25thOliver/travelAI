# app/scraping/base_scraper.py

import httpx
from bs4 import BeautifulSoup


class BaseScraper:
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    async def fetch(self, url: str) -> str:
        async with httpx.AsyncClient(
            timeout=30.0,
            headers=self.HEADERS,
            follow_redirects=True,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text

    def parse_html(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")
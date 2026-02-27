# app/scraping/destination_scraper.py

from typing import List, Dict
from bs4 import BeautifulSoup
from app.scraping.base_scraper import BaseScraper


class DestinationScraper(BaseScraper):
    LIST_URL = "https://en.wikipedia.org/wiki/Tourism_in_Kenya"

    async def scrape_destinations(self) -> List[Dict]:
        html = await self.fetch(self.LIST_URL)
        soup: BeautifulSoup = self.parse_html(html)

        destinations: List[Dict] = []

        # Extract links inside main content area
        content = soup.select_one("#mw-content-text")
        if not content:
            return destinations

        links = content.select("a[href^='/wiki/']")

        seen = set()

        for link in links:
            title = link.get_text(strip=True)
            href = link.get("href")

            if not title or ":" in href:
                continue

            if title in seen:
                continue

            seen.add(title)

            destinations.append(
                {
                    "title": title,
                    "location": "Kenya",
                    "category": "Tourism",
                    "description": f"Wikipedia reference for {title}.",
                    "source_url": f"https://en.wikipedia.org{href}",
                }
            )

        return destinations[:20]  # limit for testing
# app/scraping/destination_scraper.py

from typing import List, Dict
from bs4 import BeautifulSoup
from app.scraping.base_scraper import BaseScraper


class DestinationScraper(BaseScraper):
    BASE_URL = "https://www.magicalkenya.com"
    LIST_URL = "https://www.magicalkenya.com/places-to-visit/"

    async def scrape_destinations(self) -> List[Dict]:
        html = await self.fetch(self.LIST_URL)
        soup: BeautifulSoup = self.parse_html(html)

        destinations: List[Dict] = []

        # Each destination card
        cards = soup.select("div.card")  # main destination cards

        for card in cards:
            title_tag = card.select_one("h3.card-title")
            description_tag = card.select_one("p.card-text")
            link_tag = card.select_one("a")

            if not title_tag or not link_tag:
                continue

            title = title_tag.get_text(strip=True)
            description = (
                description_tag.get_text(strip=True)
                if description_tag
                else "No description available."
            )

            relative_url = link_tag.get("href")
            source_url = (
                relative_url
                if relative_url.startswith("http")
                else f"{self.BASE_URL}{relative_url}"
            )

            destinations.append(
                {
                    "title": title,
                    "location": "Kenya",
                    "category": "Tourism",
                    "description": description,
                    "source_url": source_url,
                }
            )

        return destinations
from app.scraping.base_scraper import BaseScraper

class DestinationScraper(BaseScraper):
    async def scrape_example(self) -> list[dict]:
        # Placeholder for real tourism source
        html = await self.fetch("https://example.com")
        soup = self.parse_html(html)

        # Selectors
        return [
            {
                "title": "Maasai Mara",
                "location": "Narok",
                "category": "Wildlife",
                "description": "Famous safari destination in Kenya.",
                "source_url": "https://example.com",
            }
        ]
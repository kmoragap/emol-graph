import random
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import RAW_DATA_PATH


class EmolScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"}
        self.base_sitemap = "https://www.emol.com/sitemap/xml/sitemap{}_2025.xml"

    def fetch_sitemap_urls(self, sitemap_ids=[1, 2, 3]):
        """Collects article URLs from specific sitemaps."""
        urls = []
        print(f"Scanning sitemaps: {sitemap_ids}...")

        for i in sitemap_ids:
            url = self.base_sitemap.format(i)
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "xml")
                    # Filter only news articles, ignore images/videos
                    new_urls = [
                        loc.text
                        for loc in soup.find_all("loc")
                        if "/noticias/" in loc.text
                        and not loc.text.endswith((".jpg", ".xml"))
                    ]
                    urls.extend(new_urls)
                    time.sleep(1)  # Be polite to the server
            except Exception as e:
                print(f"Error fetching sitemap {i}: {e}")

        # Remove duplicates
        return list(set(urls))

    def parse_article(self, url):
        """Extracts title and body from a single article."""
        try:
            time.sleep(random.uniform(0.5, 1.0))
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.content, "html.parser")

            # Emol specific selectors
            title_tag = soup.find("h1", id="cuDetalle_cuTitular_tituloNoticia")
            body_tag = soup.find("div", id="cuDetalle_cuTexto_textoNoticia")

            if not body_tag:
                return None

            return {
                "url": url,
                "title": title_tag.text.strip() if title_tag else "",
                "body": body_tag.text.strip(),
            }
        except Exception:
            return None

    def run(self, limit=500):
        """Main execution method."""
        urls = self.fetch_sitemap_urls()
        print(f"Found {len(urls)} URLs. Scraping first {limit}...")

        data = []
        for i, url in enumerate(urls[:limit]):
            article = self.parse_article(url)
            if article:
                data.append(article)

            if i % 50 == 0:
                print(f"Processed {i} articles...")

        # Save to CSV
        df = pd.DataFrame(data)
        df.to_csv(RAW_DATA_PATH, index=False)
        print(f"Done. Saved {len(df)} articles to {RAW_DATA_PATH}")


if __name__ == "__main__":
    scraper = EmolScraper()
    scraper.run(limit=1000)

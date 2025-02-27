from scraper.category_scraper import CategoryScraper
from scraper.search_scraper import SearchScraper

class ScraperManager:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape_category(self, identifier):
        category_scraper = CategoryScraper(self.base_url)
        return category_scraper.scrape(identifier)
    def scrape_search(self, identifier):
        search_scraper = SearchScraper(self.base_url)
        return search_scraper.scrape(identifier)
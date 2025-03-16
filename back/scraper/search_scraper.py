from scraper.list_scraper import ListScraper


class SearchScraper(ListScraper):
    def __init__(self, base_url):
        super().__init__(base_url, "category?q={id}")

if __name__ == "__main__":
    category_scraper = SearchScraper("https://list.am")
    print(category_scraper.scrape("mazda"))

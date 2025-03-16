from scraper.list_scraper import ListScraper


class CategoryScraper(ListScraper):
    def __init__(self, base_url):
        super().__init__(base_url, "category/{id}?gl=2")

if __name__ == "__main__":
    category_scraper = CategoryScraper("https://list.am")
    print(category_scraper.scrape("mazda"))


from time import sleep

from back.base_scraper import BaseScraper
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class ItemScraper(BaseScraper):
    def __init__(self, base_url):
        super().__init__(base_url)

    def scrape(self, identifier):
        response = self.get_data(identifier)
        soup = BeautifulSoup(response, 'html.parser')
        final_data = {}
        final_data["info"] = {
            "base_url": self.base_url
        }
        final_data["name"] = soup.find("h1").text if soup.find("h1") else None
        final_data["price"] = soup.find("span", class_='price').text if soup.find("span", class_='price') else None
        images = []
        for image_div in soup.find("div", class_='po55').find("div", class_='p').find_all("div"):
            images.append(image_div.find("img")["src"])
        final_data["images"] = images
        description = ""



    def get_data(self, url):
        full_url = self.base_url + url
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(full_url)
            # loop through all spans in .jumptodiv and click them
            for span in page.query_selector_all('.jumptodiv span'):
                span.click()

            # loop through the spans again to verify that images are loaded
            for div in page.query_selector_all('.po55 > .p'):
                # assert that the image is loaded
                assert div.query_selector('img').get_attribute('src') is not None

        return page.content()


if __name__ == "__main__":
    item_scraper = ItemScraper("https://www.list.am/")
    # item_scraper.get_data("https://www.list.am/item/21396205)
    item_scraper.get_data('item/21396205')


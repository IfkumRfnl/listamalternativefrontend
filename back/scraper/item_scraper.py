from time import sleep

from back.base_scraper import BaseScraper
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
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

        # get attributes
        final_data["attribute_blocks"] = []
        for attr_block_div in soup.find_all("div", class_='attr'):
            # get name of attribute block (which is previous div)
            attr_block_name = attr_block_div.find_previous("div").text
            # get attributes
            attributes = []
            for attr_div in attr_block_div.find_all('div', class_='c'):
                attr_name = attr_div.find("div", class_='t').text
                attr_value = attr_div.find("div", class_='i').text
                attributes.append({
                    "name": attr_name,
                    "value": attr_value
                })
            final_data["attribute_blocks"].append({
                "attr_block_name": attr_block_name,
                "attributes": attributes
            })

        # price history
        final_data['price_history'] = []
        for price in soup.find("table", class_='history').find("tbody").find_all("tr") if soup.find("table", class_='history') else []:
            td_divs = price.find_all("td")

            date = td_divs[0].text
            price = td_divs[1].text
            # check if last div has attribute class 'down' or 'up'
            is_down = td_divs[2].has_attr('class') and 'down' in td_divs[2]['class']
            price_change = td_divs[2].text
            final_data["price_history"].append({
                "date": date,
                "price": price,
                "is_down": is_down,
                "price_change": price_change
            })

        final_data["description"] = soup.find("div", class_='body').get_text() if soup.find("div", class_='body') else None

        return final_data

    def get_data(self, url):
        full_url = self.base_url + "item/" + url
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--headless=new"])
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            page = context.new_page()
            stealth_sync(page)
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
    print(item_scraper.scrape('item/22067786'))


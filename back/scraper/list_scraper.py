from back.base_scraper import BaseScraper
from bs4 import BeautifulSoup
from curl_cffi import requests
import requests_html

class ListScraper(BaseScraper):
    def __init__(self, base_url, url):
        super().__init__(base_url)
        self.url = url

    def scrape(self, identifier):
        final_data = {}


        url = f"{self.base_url}/{self.url}".format(id=identifier)
        response = self.get_data(url)
        soup = BeautifulSoup(response.content, "html.parser")

        category_name = soup.find("h1").text if soup.find("h1") else None

        final_data["info"] = {
            "base_url": self.base_url,
            "category_name": category_name
        }

        top_products = soup.find(id="tp").find("div", class_="dl").find_all('a') if soup.find(id="tp") else []
        products = []
        for top_product in top_products:
            product = self._process_product(top_product, top=True)
            products.append(product)

        regular_products = soup.find_all("div", class_="dl")[1].find_all('a', class_="fav-item-info-container") if soup.find("div", class_="dl") else []

        for regular_product in regular_products:

            product = self._process_product(regular_product)
            products.append(product)
        final_data["products"] = products

        # nav bar
        nav_bar = soup.find("div", )

        print(products)
        return final_data

    def _process_product(self, product, top=False):
        details = product.find("div")
        return {
            "top": top,
            "url": product['href'].strip() if product else None,
            "image": product.find("img")['src'].strip() if product.find("img") and product.find("img")["src"] else
                product.find("img").get("data-original") if product.find("img") else None,
            "name": details.find("div", class_="dltitle").text.strip() if details and details.find("div",
                                                                                                   class_="dltitle") else None,
            "price": details.find("div", class_="ad-info-line-wrapper").text.strip() if details and details.find("div",
                                                                                                                 class_="ad-info-line-wrapper") else None,
            "place": details.find("div", class_="at").text.strip() if details and details.find("div",
                                                                                               class_="at") else None
        }

    def get_data(self, url):
        response = requests.get(url, impersonate="chrome")
        return response






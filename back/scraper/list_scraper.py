from base_scraper import BaseScraper
from bs4 import BeautifulSoup
from curl_cffi import requests
import requests_html

class ListScraper(BaseScraper):
    def __init__(self, base_url, url):
        super().__init__(base_url)
        self.url = url

    def scrape(self, identifier):
        final_data = {}

        category_number = identifier.split("/")[0] if "/" in identifier else None


        url = f"{self.base_url}/{self.url}".format(id=identifier)
        response = self.get_data(url)
        soup = BeautifulSoup(response.content, "html.parser") if response else None

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

        regular_products = soup.find_all("div", class_="dl")[1 if len(top_products) != 0 else 0].find_all('a', class_="fav-item-info-container") if category_name else []

        for regular_product in regular_products:

            product = self._process_product(regular_product)
            products.append(product)
        final_data["products"] = products

        # nav bar
        final_data["nav_bar"] = []
        nav_bar = soup.find("div", class_="dlf").find("span", class_="pp").find_all() if soup.find("div", class_="dlf") else []
        for i, nav in enumerate(nav_bar):
            final_data["nav_bar"].append({
                "url": f"/category/{category_number}/{i+1}",
                "page": nav.text.strip() if nav else None,
                "active": nav.name == "span"
            })




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






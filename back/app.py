from flask import Flask, jsonify, render_template, request

from scraper_manager import ScraperManager  # Import your scraper managero
from config import Config


app = Flask(__name__)
app.template_folder = Config.template_folder
app.static_folder = Config.static_folder


base_url = 'https://list.am'
scraper_manager = ScraperManager(base_url)

@app.route('/api/category/<identifier>', methods=['GET'])
def category_api(identifier):
    # Get category data from your scraper
    category_data = scraper_manager.scrape_category(identifier)
    return jsonify(category_data)

@app.route('/category/<identifier>/<int:page>', methods=['GET'])
@app.route('/category/<identifier>', methods=['GET'])
def category(identifier, page=1):
    identifier=f"{identifier}/{page}"
    # Get category data from your scraper
    category_data = scraper_manager.scrape_category(identifier)
    return render_template('category.html', category_data=category_data)

@app.route('/api/category?q=<query>', methods=['GET'])
def category_search_api(query):
    # Get category data from your scraper
    category_data = scraper_manager.scrape_category(query)
    return jsonify(category_data)

@app.route('/category', methods=['GET'])
def category_search():
    query = request.args.get('q')
    # Get category data from your scraper
    category_data = scraper_manager.scrape_search(query)
    return render_template('category.html', category_data=category_data)


if __name__ == '__main__':
    app.run(debug=True)

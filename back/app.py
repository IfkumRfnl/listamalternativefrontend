import mimetypes

from flask import Flask, jsonify, render_template, request, send_from_directory

from scraper_manager import ScraperManager  # Import your scraper managero
from config import Config
import os


app = Flask(__name__)
app.template_folder = Config.template_folder
app.static_folder = Config.static_folder


base_url = 'https://list.am/'
CACHE_DIR = 'f'
scraper_manager = ScraperManager(base_url)

@app.route('/')
def index():
    return render_template('home.html')

@app.route(f'/{CACHE_DIR}/<product_key>/<filename>', methods=['GET'])
def get_image(product_key, filename):
    directory = os.path.join(app.root_path, CACHE_DIR, product_key)
    filepath = os.path.join(directory, filename)

    # Determine MIME type based on extension
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    mime_type = mime_types.get(ext, 'application/octet-stream')  # Default to binary if unknown

    # Serve the file with explicit MIME type
    response = send_from_directory(directory, filename)
    response.headers['Content-Type'] = mime_type
    response.headers['Content-Disposition'] = 'inline'
    return response



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

@app.route('/api/item/<identifier>', methods=['GET'])
def item_api(identifier):
    # Get item data from your scraper
    item_data = scraper_manager.scrape_item(identifier)
    return jsonify(item_data)

@app.route('/item/<identifier>', methods=['GET'])
def item(identifier):
    # Get item data from your scraper
    item_data = scraper_manager.scrape_item(identifier)
    return render_template('item.html', item_data=item_data)


if __name__ == '__main__':
    app.run(debug=True)

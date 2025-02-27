from pathlib import Path

# Get the project root directory (parent of backend)
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the front-end directory which contains the static and templates folders
FRONT_DIR = BASE_DIR / 'front'

# Paths to the templates and static directories
TEMPLATE_DIR = FRONT_DIR / 'templates'
STATIC_DIR = FRONT_DIR / 'static'

class Config:
    DEBUG = True
    # Configuration for Flask to locate templates and static files
    template_folder = str(TEMPLATE_DIR)
    static_folder = str(STATIC_DIR)

import sqlite3
import os
from curl_cffi import requests
import time
from typing import Dict, Any, Optional
import shutil
from pathlib import Path


class CacheManager:
    def __init__(self, db_path: str = 'cache_db', cache_dir: str = "f", ttl: int = 3600):
        """
        Initialize CacheManager with database path, cache directory and TTL.

        Args:
            db_path (str): Path to SQLite database file
            cache_dir (str): Directory to store downloaded images
            ttl (int): Time to live in seconds (default: 1 hour)
        """
        self.db_path = db_path
        self.cache_dir = cache_dir
        self.ttl = ttl

        # Create cache directory if it doesn't exist
        Path(cache_dir).mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite database with required table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    data TEXT,
                    images TEXT,
                    timestamp INTEGER
                )
            """)
            conn.commit()

    def _download_image(self, url: str, product_key: str) -> str:
        """
        Download image from URL and save it locally.

        Args:
            url (str): Image URL
            product_key (str): Unique identifier for the product

        Returns:
            str: Local path to downloaded image
        """
        try:
            if url.startswith("//"):
                url = "https:" + url
            # https://s.list.am/f/291/83964291.webp
            local_dir = os.path.join('back', self.cache_dir, product_key)
            print(f"Downloading image from {url} to {local_dir}")
            os.makedirs(local_dir, exist_ok=True)
            local_path = os.path.join(local_dir, os.path.basename(url))
            if os.path.exists(local_path):
                print(f"Image already exists at {local_path}")
                return local_path
            response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"}, timeout=10, stream=True)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            remote_path = f"/{self.cache_dir}/{product_key}/{os.path.basename(url)}"
            print(f"Image downloaded and saved to {local_path}")
            return remote_path
        except Exception as e:
            print(f"Error downloading image {url}: {str(e)}")
            return ""

    def set(self, key: str, data: Dict[str, Any]) -> bool:
        """
        Store data in cache and download associated images.

        Args:
            key (str): Unique identifier for the product
            data (dict): Product data including 'images' list

        Returns:
            bool: Success status
        """
        try:
            # Handle images if present
            image_urls = data.get('images', [])
            local_image_paths = []

            for url in image_urls:
                if url:
                    local_path = self._download_image(url, url.split('/')[4])
                    if local_path:
                        local_image_paths.append(local_path)

            # Convert data to string for storage (excluding original images)
            data_to_store = {k: v for k, v in data.items() if k != 'images'}
            data_str = str(data_to_store)
            images_str = ','.join(local_image_paths)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO cache (key, data, images, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (key, data_str, images_str, int(time.time())))
                conn.commit()
            return True

        except Exception as e:
            print(f"Error setting cache for {key}: {str(e)}")
            return False

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from cache if not expired.

        Args:
            key (str): Product identifier

        Returns:
            dict or None: Cached data with local image paths if available and not expired
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT data, images, timestamp 
                    FROM cache 
                    WHERE key = ?
                """, (key,))

                result = cursor.fetchone()
                if result:
                    data_str, images_str, timestamp = result

                    # Check if cache is still valid
                    if int(time.time()) - timestamp > self.ttl:
                        # Delete expired entry
                        cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
                        conn.commit()
                        return None

                    # Parse stored data
                    data = eval(data_str)  # Note: eval() is used for simplicity, consider json in production
                    if images_str:
                        data['images'] = images_str.split(',')

                    return data
                return None

        except Exception as e:
            print(f"Error getting cache for {key}: {str(e)}")
            return None


# Example usage:


import requests

import requests
from pathlib import Path
import hashlib
import os

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

if not all([PEXELS_API_KEY, UNSPLASH_ACCESS_KEY, PIXABAY_API_KEY]):
    raise EnvironmentError("❌ Alguna clave API no está definida en el archivo .env")
print("✅ Todas las claves API están definidas correctamente.")


def download_image_lorem_picsum(query: str, image_name: str, width=1280, height=720) -> str:
    """
    Downloads a random landscape image from Lorem Picsum using a seed derived from the query.
    Saves it under the 'images/' folder with the specified image_name.

    Returns:
        str: Path to the saved image.
    """
    if not query.strip() or not image_name.strip():
        print("Both categories and image_name must be provided.")
        return ""

    # Use hash of categories string as seed to get consistent images
    seed = hashlib.md5(query.encode('utf-8')).hexdigest()
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}"

    try:
        image_dir = Path("images")
        image_dir.mkdir(parents=True, exist_ok=True)
        image_path = image_dir / image_name

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(image_path, "wb") as file:
            file.write(response.content)

        return str(image_path)

    except requests.RequestException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return ""


def download_image_pixabay(query: str, image_name: str) -> str:
    """
    Downloads a landscape image from Pixabay based on given query.
    Saves it under the 'images/' folder with the specified image_name.

    Returns:
        str: Path to the saved image, or empty string if not found.
    """
    if not query.strip() or not image_name.strip():
        print("Both categories and image_name must be provided.")
        return ""

    url = "https://pixabay.com/api/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "orientation": "horizontal",
        "per_page": 3
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("hits"):
            print(f"No results found on Pixabay for: {query}")
            return ""

        image_url = data["hits"][0]["largeImageURL"]

        image_dir = Path("images")
        image_dir.mkdir(parents=True, exist_ok=True)
        image_path = image_dir / image_name

        img_response = requests.get(image_url, timeout=10)
        img_response.raise_for_status()

        with open(image_path, "wb") as file:
            file.write(img_response.content)

        return str(image_path)

    except requests.exceptions.RequestException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return ""


def download_image_unsplash(query: str, image_name: str) -> str:
    """Downloads a landscape image from Unsplash based on given query."""

    if not query.strip() or not image_name.strip():
        print("categories and image_name cannot be empty")
        return ""

    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": query,
        "orientation": "landscape",
        "per_page": 1,
        "page": 1
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            print(f"No images found for: {query}")
            return ""

        photo = results[0]
        image_url = photo["urls"]["regular"]

        image_dir = Path("images")
        image_dir.mkdir(exist_ok=True, parents=True)
        image_path = image_dir / image_name

        img_resp = requests.get(image_url, timeout=10)
        img_resp.raise_for_status()
        with open(image_path, "wb") as f:
            f.write(img_resp.content)

        return str(image_path)

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return ""


def download_image_pexels(query: str, image_name: str) -> str:
    """
    Downloads a landscape image from Pexels based on given query.
    Saves it under the 'images/' folder with the specified image_name.

    Returns:
        str: Path to the saved image, or empty string if not found.
    """

    if not query.strip() or not image_name.strip():
        print("Both categories and image_name must be provided.")
        return ""

    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": query,
        "orientation": "landscape",
        "per_page": 1,
        "page": 1
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("photos"):
            print(f"No results found on Pexels for: {query}")
            return ""

        photo = data["photos"][0]
        image_url = photo["src"]["large"]

        # Prepare path
        image_dir = Path("images")
        image_dir.mkdir(parents=True, exist_ok=True)
        image_path = image_dir / image_name

        # Download image
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        with open(image_path, "wb") as file:
            file.write(img_response.content)

        return str(image_path)

    except requests.exceptions.RequestException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return ""


def download_image_api(query: str, image: str) -> str:
    """
    Tries to download an image using a list of query from multiple APIs:
    Pexels → Unsplash → Pixabay → Lorem Picsum.

    Returns:
        str: Path to the downloaded image or empty string if all APIs fail.
    """
    query = query.strip()
    if not query or not image:
        print("query and image name are required.")
        return ""

    # Try Pexels
    path = download_image_pexels(query, image)
    if path:
        print(f"🔍 Searching image for: '{query}' ✅ Image found using Pexels.")
        return path

    # Try Unsplash
    path = download_image_unsplash(query, image)
    if path:
        print(f"🔍 Searching image for: '{query}' ✅ Image found using Unsplash.")
        return path

    # Try Pixabay
    path = download_image_pixabay(query, image)
    if path:
        print(f"🔍 Searching image for: '{query}' ✅ Image found using Pixabay.")
        return path

    # Fallback: Lorem Picsum (no real search, just a seed)
    path = download_image_lorem_picsum(query, image)
    if path:
        print(f"🔍 Searching image for: '{query}' 🖼️ Fallback image used from Lorem Picsum.")
        return path

    print(f"🔍 Searching image for: '{query}' ❌ No image could be downloaded from any source.")
    return ""

def find_image_bulk(queries: list, image_names: list) -> list:
    """
    Downloads images for a list of queries and image names.
    Returns a list of paths to the downloaded images.
    """
    if len(queries) != len(image_names):
        raise ValueError("The length of queries and image_names must be the same.")

    image_paths = []
    for query, image_name in zip(queries, image_names):
        path = download_image_api(query, image_name)
        if path:
            image_paths.append(path)

    return image_paths


def main():
    query = ["Wok To Walk - Pizza - Kebab", "NuPoo Pizza&Burger Vršovice", "Shell"]
    image_name = ["restaurant_food.jpg", "landscape.jpg", "city_skyline.jpg"]
    image_path = find_image_bulk(query, image_name)


if __name__ == "__main__":
    main()
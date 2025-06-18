import json
import sqlite3
from pathlib import Path

def convert_json_to_sqlite(json_posts: Path, json_categories: Path, db_file: Path):

    # Leer JSONs
    with open(json_categories, "r", encoding="utf-8") as f:
        categories = json.load(f)

    with open(json_posts, "r", encoding="utf-8") as f:
        posts = json.load(f)

    # Crear conexión y cursor
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Crear tabla pages
    cur.execute("DROP TABLE IF EXISTS pages;")
    cur.execute("""
    CREATE TABLE pages (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        slug TEXT NOT NULL,
        content TEXT NOT NULL,
        image TEXT
    );
    """)

    # Crear tabla categories
    cur.execute("DROP TABLE IF EXISTS categories;")
    cur.execute("""
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        slug TEXT NOT NULL
    );
    """)
    for c in categories:
        cur.execute("INSERT INTO categories (id, name, slug) VALUES (?, ?, ?)", (c["id"], c["name"], c["slug"]))

    # Crear tabla posts
    cur.execute("DROP TABLE IF EXISTS posts;")
    cur.execute("""
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY,
        title TEXT,
        slug TEXT,
        rating REAL,
        reviews INTEGER,
        reviews_link TEXT,
        web_url TEXT,
        web_url_root TEXT,
        phone TEXT,
        image_1 TEXT,
        image_2 TEXT,
        image_3 TEXT,
        categories TEXT,
        address TEXT,
        google_maps_url TEXT,
        price_range TEXT,
        zipcode TEXT,
        city TEXT,
        state TEXT,
        hoary TEXT,
        link_menu TEXT,
        link_reservations TEXT,
        link_order_online TEXT,
        content TEXT,
        category_id INTEGER,
        image TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );
    """)

    # Insertar posts
    for p in posts:
        cur.execute("""
        INSERT INTO posts (
            id, title, slug, rating, reviews, reviews_link, web_url, web_url_root,
            phone, image_1, image_2, image_3, categories, address, google_maps_url,
            price_range, zipcode, city, state, hoary, link_menu, link_reservations,
            link_order_online, content, category_id, image
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["title"], p["slug"], p["rating"], p["reviews"], p["reviews_link"],
            p["web_url"], p["web_url_root"], p["phone"], p["image_1"], p["image_2"], p["image_3"],
            p["categories"], p["address"], p["google_maps_url"], p["price_range"], p["zipcode"],
            p["city"], p["state"], p["hoary"], p["link_menu"], p["link_reservations"],
            p["link_order_online"], p["content"], p["category_id"], p["image"]
        ))

    # Guardar y cerrar
    conn.commit()
    conn.close()

    print(f"✅ Base de datos creada: {db_file.resolve()}")

if __name__ == "__main__":
    # Carpetas
    BASE_DIR = Path(__file__).resolve().parent
    BASE_OUTPUT_DIR = BASE_DIR / "output"

    # Categorías y posts
    FILE_CATEGORIES_JSON = BASE_OUTPUT_DIR / "categories.json"
    FILE_POSTS_JSON = BASE_OUTPUT_DIR / "posts.json"
    DB_FILENAME = BASE_OUTPUT_DIR / "blog.db"

    # Convertimos los archivos JSON de posts y categorías a una base de datos SQLite
    convert_json_to_sqlite(
        json_posts=FILE_POSTS_JSON,
        json_categories=FILE_CATEGORIES_JSON,
        db_file=DB_FILENAME,
    )
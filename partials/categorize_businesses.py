import json
import os
from pathlib import Path

from partials.helpers import slugify


def get_category_name(row):
    city = (row.get("city") or "").strip()
    state = (row.get("state") or "").strip()
    return city or state or "Others"


def generate_categories_from_posts_json(posts_file: Path, output_posts_file: Path, categories_file: Path):
    categories = {}
    next_id = 1

    # Cargar categorías existentes
    if os.path.exists(categories_file):
        with open(categories_file, encoding='utf-8') as f:
            categories_data = json.load(f)
            for item in categories_data:
                categories[item["name"]] = {
                    "id": int(item["id"]),
                    "slug": item["slug"]
                }
            if categories:
                next_id = max(c["id"] for c in categories.values()) + 1

    # Leer posts
    with open(posts_file, encoding='utf-8') as f:
        posts = json.load(f)
        if not posts:
            print("⚠️ El archivo de posts está vacío.")
            return

    # Crear mapeo nombre_categoria → category_id
    name_to_id = {}
    for post in posts:
        category_name = get_category_name(post)
        if category_name not in categories:
            categories[category_name] = {
                "id": next_id,
                "slug": slugify(category_name)
            }
            next_id += 1
        name_to_id[category_name] = categories[category_name]["id"]

    # Guardar categories.json
    with open(categories_file, "w", encoding='utf-8') as f:
        categorias_list = [
            {"id": data["id"], "name": name, "slug": data["slug"]}
            for name, data in sorted(categories.items(), key=lambda x: x[1]["id"])
        ]
        json.dump(categorias_list, f, ensure_ascii=False, indent=2)

    # Añadir category_id a posts y guardar nuevo archivo
    for post in posts:
        category_name = get_category_name(post)
        post["category_id"] = name_to_id[category_name]

    with open(output_posts_file, "w", encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"✅ '{os.path.basename(categories_file)}' y '{os.path.basename(output_posts_file)}' fueron creados/modificados correctamente.")

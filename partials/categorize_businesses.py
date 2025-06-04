import csv
import os

from partials.helpers import slugify

def generate_categories_from_posts(posts_file: str, output_posts_file: str, categories_file: str = "categories.csv"):
    # Cargar categorías existentes
    categories = {}
    next_id = 1

    if os.path.exists(categories_file):
        with open(categories_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                categories[row["name"]] = {
                    "id": int(row["id"]),
                    "slug": row["slug"]
                }
            if categories:
                next_id = max(c["id"] for c in categories.values()) + 1

    # Leer posts
    with open(posts_file, newline='', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        if not reader:
            print("⚠️ El archivo de posts está vacío.")
            return
        fieldnames = reader[0].keys()

    # Crear mapeo city → category_id y actualizar si es necesario
    city_to_id = {}
    for row in reader:
        city = row["city"].strip() or "Others"  # <-- Aquí se asigna "Others" si city está vacío
        if city not in categories:
            categories[city] = {
                "id": next_id,
                "slug": slugify(city)
            }
            next_id += 1
        city_to_id[city] = categories[city]["id"]

    # Guardar categories.csv
    with open(categories_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "slug"])
        writer.writeheader()
        for name, data in sorted(categories.items(), key=lambda x: x[1]["id"]):
            writer.writerow({
                "id": data["id"],
                "name": name,
                "slug": data["slug"]
            })

    # Añadir category_id a posts
    new_fieldnames = list(fieldnames) + ["category_id"] if "category_id" not in fieldnames else list(fieldnames)

    with open(output_posts_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        for row in reader:
            city = row["city"].strip() or "Others"
            row["category_id"] = city_to_id[city]
            writer.writerow(row)

    print(f"✅ '{os.path.basename(categories_file)}' y '{os.path.basename(output_posts_file)}' fueron creados/modificados correctamente.")

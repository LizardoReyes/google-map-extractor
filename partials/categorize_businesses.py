import json
import os
import pandas as pd

from pathlib import Path
from partials.helpers import slugify


def get_category_name(row):
    city = (row.get("city") or "").strip()
    return city or "Others"


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


""" Estas funciones son para agregar nuevos negocios y categorías a los archivos JSON existentes."""

def merge_json_files_unique(
        file_a: Path,
        file_b: Path,
        output_file: Path,
        unique_key: str = "slug"
):
    """
    Une dos archivos JSON que contienen listas de objetos y elimina duplicados según unique_key.

    Args:
        file_a (Path): Ruta al primer archivo JSON.
        file_b (Path): Ruta al segundo archivo JSON.
        output_file (Path): Ruta de salida del JSON combinado.
        unique_key (str): Clave para considerar elementos duplicados (por defecto: 'slug').
    """
    try:
        df_a = pd.read_json(file_a)
    except Exception:
        df_a = pd.DataFrame()

    try:
        df_b = pd.read_json(file_b)
    except Exception:
        df_b = pd.DataFrame()

    df_combined = pd.concat([df_a, df_b], ignore_index=True)

    if unique_key in df_combined.columns:
        df_combined = (df_combined.drop_duplicates(subset="title", keep="first")
                       .drop_duplicates(subset=unique_key, keep="first"))

    df_combined.to_json(output_file, orient="records", indent=2, force_ascii=False)
    print(
        f"✅ Archivos '{file_a.name}' + '{file_b.name}' combinados sin duplicados por '{unique_key}' en: {output_file}")
    print(f"✅ Total de filas únicas combinadas: ({len(df_combined)} negocios)")


def merge_categories_and_generate_unique_new_posts(
    posts_file: Path,
    new_posts_file: Path,
    categories_file: Path,
    output_new_posts_file: Path,
    output_categories_file: Path
):
    # Leer posts existentes y nuevos
    df_posts = pd.read_json(posts_file)
    df_new = pd.read_json(new_posts_file)

    # Eliminar duplicados internos en los nuevos por 'slug' y luego por 'title'
    df_new = (
        df_new.drop_duplicates(subset="slug", keep="first")
              .drop_duplicates(subset="title", keep="first")
    )

    # Obtener slugs y titles ya existentes en los posts actuales
    existing_slugs = set(df_posts["slug"])
    existing_titles = set(df_posts["title"])

    # Eliminar duplicados externos por slug y title (comparando con df_posts)
    df_new = df_new[~df_new["slug"].isin(existing_slugs)]
    df_new = df_new[~df_new["title"].isin(existing_titles)]

    # Asignar nuevos ID a los nuevos posts
    max_post_id = df_posts["id"].max() if not df_posts.empty else 0
    df_new["id"] = range(max_post_id + 1, max_post_id + 1 + len(df_new))

    # Leer categorías existentes
    df_cat = pd.read_json(categories_file) if categories_file.exists() else pd.DataFrame(columns=["id", "name", "slug"])

    # Unificar ciudades como posibles categorías
    all_cities = pd.concat([df_posts["city"], df_new["city"]]).dropna().unique()
    df_new_cats = pd.DataFrame({
        "name": all_cities,
        "slug": [slugify(city) for city in all_cities]
    })

    # Combinar categorías y eliminar duplicados por slug
    df_combined_cats = pd.concat([df_cat, df_new_cats], ignore_index=True)
    df_combined_cats = df_combined_cats.drop_duplicates(subset="slug", keep="first")

    # Asignar ID a nuevas categorías que no lo tienen
    if "id" not in df_combined_cats or df_combined_cats["id"].isnull().all():
        df_combined_cats["id"] = None
    max_cat_id = df_combined_cats["id"].dropna().max() if not df_combined_cats["id"].dropna().empty else 0

    mask_missing_id = df_combined_cats["id"].isnull()
    df_combined_cats.loc[mask_missing_id, "id"] = range(
        int(max_cat_id) + 1,
        int(max_cat_id) + 1 + mask_missing_id.sum()
    )
    df_combined_cats["id"] = df_combined_cats["id"].astype(int)

    # Mapear city → category_id
    city_slug_map = pd.DataFrame({
        "city": all_cities,
        "slug": [slugify(city) for city in all_cities]
    })
    merged_map = pd.merge(city_slug_map, df_combined_cats, on="slug", how="left")
    city_to_id = dict(zip(merged_map["city"], merged_map["id"]))

    df_new["category_id"] = df_new["city"].map(city_to_id)

    # Guardar resultados
    df_new.to_json(output_new_posts_file, orient="records", indent=2, force_ascii=False)
    df_combined_cats.sort_values("id").to_json(output_categories_file, orient="records", indent=2, force_ascii=False)

    print(f"✅ Nuevos negocios únicos guardados en: {output_new_posts_file}")
    print(f"✅ Categorías consolidadas en: {output_categories_file}")
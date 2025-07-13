"""Script para procesar negocios faltantes y buscar una imagen para cada uno."""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from converts.convert_json_to_csv import convert_json_to_csv
from converts.convert_json_to_sqlite import convert_json_to_sqlite
from enums.Language import Language
from partials.categorize_businesses import generate_categories_from_posts_json
from partials.generate_images_json_and_names import generate_images_json_and_names
from partials.helper_csv import merge_json_in_folder, filter_businesses, \
    save_business, read_csv_full
from partials.helpers import create_business, delete_files
from helpers.find_image_bulk import find_image_bulk


def prepare_search_terms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea una nueva columna 'search_term' usando 'categories' si existe y no está vacía;
    de lo contrario usa 'title'.
    """
    def get_term(row):
        categories = row.get("categories", "")
        title = row.get("title", "")
        return categories if str(categories).strip() else str(title).strip()

    df["search_term"] = df.apply(get_term, axis=1)
    return df


def main():
    faltantes_df = read_csv_full(FILE_FALTANTES_CSV)
    if faltantes_df.empty:
        print("✅ No hay negocios faltantes para procesar.")
        return

    print(f"🔍 Procesando {len(faltantes_df)} negocios faltantes...")

    # Preparar columna de búsqueda
    faltantes_df = prepare_search_terms(faltantes_df)

    image_names = faltantes_df["image"].fillna("").tolist()
    search_terms = faltantes_df["search_term"].tolist()

    find_image_bulk(search_terms, image_names)


if __name__ == "__main__":

    # Carpetas
    BASE_DIR = Path(__file__).resolve().parent
    BASE_OUTPUT_DIR = BASE_DIR / "output"
    DIR_IMAGES = BASE_DIR / "images"

    # Categorías y posts
    FILE_FALTANTES_CSV = BASE_OUTPUT_DIR / "faltantes.csv"


    main()

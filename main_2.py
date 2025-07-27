"""
    Script para procesar negocios faltantes y BUSCAR IMAGEN para cada uno.
"""

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


def main():
    faltantes_df = read_csv_full(FILE_FALTANTES_CSV)
    if faltantes_df.empty:
        print("✅ No hay negocios faltantes para procesar.")
        return

    print(f"🔍 Procesando {len(faltantes_df)} negocios faltantes...")

    # Obtener los campos necesarios de los negocios faltantes
    titles = faltantes_df["title"].tolist()
    images = faltantes_df["image"].fillna("").tolist()
    categories = faltantes_df["categories"].tolist()
    cities = faltantes_df["city"].tolist()

    find_image_bulk(titles, images)


if __name__ == "__main__":

    # Carpetas
    BASE_DIR = Path(__file__).resolve().parent
    BASE_INPUT_DIR = BASE_DIR / "input"
    DIR_IMAGES = BASE_DIR / "images"

    # Categorías y posts
    FILE_FALTANTES_CSV = BASE_INPUT_DIR / "faltantes.csv"


    main()

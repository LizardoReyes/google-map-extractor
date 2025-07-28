"""
    SCRIPT QUICKSCRAPE para procesar negocios y generar archivos JSON, CSV y SQLite.
"""
import os
from pathlib import Path

from converts.convert_json_to_csv import convert_json_to_csv
from converts.convert_json_to_sqlite import convert_json_to_sqlite
from enums.Language import Language
from parse_csv_fields import parse_csv_fields_to_json
from partials.categorize_businesses import generate_categories_from_posts_json
from partials.generate_images_json_and_names import generate_images_json_and_names
from partials.helper_csv import merge_json_folder, read_json_full, filter_businesses, \
    save_business, merge_csv_folder, read_csv_full, save_business_2
from partials.helpers import create_business, delete_files, create_bussiness_2


def main():
    # Unir los archivos JSON de la carpeta "businesses" y guardarlos en un unico archivo JSON
    merge_csv_folder(carpeta=DIR_BUSINESSES, salida=FILE_BUSINESSES_CSV_RAW)

    # Leemos un archivo CSV, creamos objetos Business y guardamos en un nuevo archivo JSON
    parse_csv_fields_to_json(input_csv=FILE_BUSINESSES_CSV_RAW, output_json=FILE_BUSINESSES_JSON)
    raw_data = read_json_full(ruta_archivo=FILE_BUSINESSES_JSON)
    business = create_bussiness_2(raw_data)
    save_business_2(business=business, ruta_salida=FILE_BUSINESSES_JSON, lang=LANGUAGE)

    # Filtramos los negocios por ciertas condiciones
    filter_businesses(nombre_archivo_json=FILE_BUSINESSES_JSON, ruta_salida=FILE_BUSINESSES_FILTERED, id_inicio=1)

    # Generamos las categorías a partir de los posts y guardamos en un nuevo archivo CSV
    generate_categories_from_posts_json(posts_file=FILE_BUSINESSES_FILTERED,
                                        output_posts_file=FILE_BUSINESSES_CATEGORIZED,
                                        categories_file=FILE_CATEGORIES_JSON)

    # Agregamos el campo imagen a los negocios en el CSV filtrado y categorizado
    generate_images_json_and_names(input_json=FILE_BUSINESSES_CATEGORIZED,
                                   output_json=FILE_BUSINESSES_WITH_IMAGES,
                                   output_image_json=FILE_IMAGE_JSON)

    # Eliminamos los archivos temporales de negocios
    delete_files(
        [FILE_BUSINESSES_JSON_RAW, FILE_BUSINESSES_CSV_RAW, FILE_BUSINESSES_JSON, FILE_BUSINESSES_FILTERED,
         FILE_BUSINESSES_CATEGORIZED, FILE_POSTS_CSV, FILE_POSTS_JSON])
    os.rename(FILE_BUSINESSES_WITH_IMAGES, FILE_POSTS_JSON)

    # Creamos la version en CSV
    convert_json_to_csv(json_path=FILE_POSTS_JSON, csv_path=FILE_POSTS_CSV)
    convert_json_to_csv(json_path=FILE_CATEGORIES_JSON, csv_path=FILE_CATEGORIES_CSV)

    # Convertimos los archivos JSON de posts y categorías a una base de datos SQLite
    convert_json_to_sqlite(
        json_posts=FILE_POSTS_JSON,
        json_categories=FILE_CATEGORIES_JSON,
        db_file=DB_FILENAME,
    )


if __name__ == "__main__":

    #############################
    # Configuración de idioma
    LANGUAGE = Language.FI
    #############################

    # Carpetas
    BASE_DIR = Path(__file__).resolve().parent
    BASE_OUTPUT_DIR = BASE_DIR / "output"
    DIR_BUSINESSES = BASE_DIR / "businesses"
    DIR_IMAGES = BASE_DIR / "images"

    # Categorías y posts
    FILE_CATEGORIES_JSON = BASE_OUTPUT_DIR / "categories.json"
    FILE_CATEGORIES_CSV = BASE_OUTPUT_DIR / "categories.csv"
    FILE_POSTS_JSON = BASE_OUTPUT_DIR / "posts.json"
    FILE_POSTS_CSV = BASE_OUTPUT_DIR / "posts.csv"

    # Archivos JSON y CSV
    FILE_BUSINESSES_JSON_RAW = BASE_OUTPUT_DIR / "businesses_raw.json"
    FILE_BUSINESSES_CSV_RAW = BASE_OUTPUT_DIR / "businesses_raw.csv"
    FILE_BUSINESSES_JSON = BASE_OUTPUT_DIR / "businesses.json"
    FILE_BUSINESSES_FILTERED = BASE_OUTPUT_DIR / "businesses_filtered.json"
    FILE_BUSINESSES_CATEGORIZED = BASE_OUTPUT_DIR / "businesses_final.json"
    FILE_BUSINESSES_WITH_IMAGES = BASE_OUTPUT_DIR / "businesses_final_image.json"
    FILE_IMAGE_JSON = BASE_OUTPUT_DIR / "images.json"
    DB_FILENAME = BASE_OUTPUT_DIR / "blog.db"

    main()

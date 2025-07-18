""" Script cuando tengas que agregar nuevos negocios a un directorio con datos ya 
    - Es necesario que existan los archivos:
        - output/posts.json
        - output/categories.json
"""
from pathlib import Path

from converts.convert_json_to_csv import convert_json_to_csv
from converts.convert_json_to_sqlite import convert_json_to_sqlite
from enums.Language import Language
from partials.categorize_businesses import merge_json_files_unique, merge_categories_and_generate_unique_new_posts, \
    deduplicate_categories_by_slug_and_fix_posts
from partials.generate_images_json_and_names import generate_images_json_and_names
from partials.helper_csv import merge_json_in_folder, read_json_full, save_business, filter_businesses
from partials.helpers import create_business, delete_files


def main():

    # Esto es para arreglar el archivo original de posts.json y categories.json
    deduplicate_categories_by_slug_and_fix_posts(
        posts_file=FILE_POSTS_ORIGINAL_JSON,
        categories_file=FILE_CATEGORIES_ORIGINAL_JSON,
        output_posts_file=FILE_POSTS_ORIGINAL_JSON,
        output_categories_file=FILE_CATEGORIES_ORIGINAL_JSON,
    )

    # Unir los archivos JSON de la carpeta "businesses" y guardarlos en un unico archivo JSON
    merge_json_in_folder(carpeta=DIR_BUSINESSES, ruta_salida=FILE_BUSINESSES_JSON_RAW)

    # Leemos un archivo JSON, creamos objetos Business y guardamos en un nuevo archivo JSON
    raw_data = read_json_full(ruta_archivo=FILE_BUSINESSES_JSON_RAW)
    business = create_business(raw_data)
    save_business(business=business, ruta_salida=FILE_BUSINESSES_JSON, lang=LANGUAGE)

    # Filtramos los negocios por ciertas condiciones
    filter_businesses(nombre_archivo_json=FILE_BUSINESSES_JSON, ruta_salida=FILE_BUSINESSES_FILTERED, id_inicio=1)

    # Ahora mezclamos los posts existentes con los nuevos negocios y generamos las categorías
    merge_categories_and_generate_unique_new_posts(
        # Posts ya existentes
        posts_file=FILE_POSTS_ORIGINAL_JSON,
        # Archivo de categorías existente
        categories_file=FILE_CATEGORIES_ORIGINAL_JSON,
        # Nuevos posts a agregar
        new_posts_file=FILE_BUSINESSES_FILTERED,
        # Archivo de salida de nuevos posts filtrados
        output_new_posts_file=FILE_PRE_NEW_POSTS_JSON,
        # Archivo de salida para las categorías combinadas
        output_categories_file=FILE_MERGED_CATEGORIES_JSON,
    )

    # Agregamos el campo imagen a los negocios en el JSON filtrado y categorizado
    generate_images_json_and_names(input_json=FILE_PRE_NEW_POSTS_JSON,
                                   output_json=FILE_NEW_POSTS_JSON,
                                   output_image_json=FILE_IMAGE_JSON)

    # Ahora combinamos los posts originales con los nuevos posts
    merge_json_files_unique(
        file_a=FILE_POSTS_ORIGINAL_JSON,
        file_b=FILE_NEW_POSTS_JSON,
        output_file=FILE_MERGED_POSTS_JSON,
        unique_key="slug"
    )

    # Creamos la version en CSV
    convert_json_to_csv(json_path=FILE_NEW_POSTS_JSON, csv_path=FILE_NEW_POSTS_CSV)
    convert_json_to_csv(json_path=FILE_MERGED_POSTS_JSON, csv_path=FILE_MERGED_POSTS_CSV)
    convert_json_to_csv(json_path=FILE_MERGED_CATEGORIES_JSON, csv_path=FILE_MERGED_CATEGORIES_CSV)

    # Eliminamos los archivos temporales de negocios
    delete_files([FILE_BUSINESSES_JSON, FILE_BUSINESSES_FILTERED, FILE_PRE_NEW_POSTS_JSON])
    # os.rename(FILE_BUSINESSES_WITH_IMAGES, FILE_NEW_POSTS_JSON)

    # Convertimos los archivos JSON de posts y categorías a una base de datos SQLite
    convert_json_to_sqlite(
        json_posts=FILE_MERGED_POSTS_JSON,
        json_categories=FILE_MERGED_CATEGORIES_JSON,
        db_file=DB_FILENAME,
    )


if __name__ == "__main__":

    #############################
    # Configuración de idioma
    LANGUAGE = Language.CS
    #############################

    # Carpetas
    BASE_DIR = Path(__file__).resolve().parent
    BASE_INPUT_DIR = BASE_DIR / "input"
    BASE_OUTPUT_DIR = BASE_DIR / "output"
    DIR_BUSINESSES = BASE_DIR / "businesses"
    DIR_IMAGES = BASE_DIR / "images"

    # Categorías y posts
    FILE_POSTS_ORIGINAL_JSON = BASE_INPUT_DIR / "posts.json"
    FILE_POSTS_ORIGINAL_JSON2 = BASE_INPUT_DIR / "posts2.json"
    FILE_POSTS_ORIGINAL_CSV = BASE_INPUT_DIR / "posts.csv"
    FILE_CATEGORIES_ORIGINAL_JSON = BASE_INPUT_DIR / "categories.json"
    FILE_CATEGORIES_ORIGINAL_JSON2 = BASE_INPUT_DIR / "categories2.json"
    FILE_CATEGORIES_ORIGINAL_CSV = BASE_INPUT_DIR / "categories.csv"

    FILE_MERGED_CATEGORIES_JSON = BASE_OUTPUT_DIR / "categories.json"
    FILE_MERGED_CATEGORIES_CSV = BASE_OUTPUT_DIR / "categories.csv"
    FILE_NEW_POSTS_JSON = BASE_OUTPUT_DIR / "posts_news.json"
    FILE_NEW_POSTS_CSV = BASE_OUTPUT_DIR / "posts_news.csv"
    FILE_MERGED_POSTS_JSON = BASE_OUTPUT_DIR / "posts.json"
    FILE_MERGED_POSTS_CSV = BASE_OUTPUT_DIR / "posts.csv"

    # Archivos JSON y CSV
    FILE_BUSINESSES_JSON_RAW = BASE_OUTPUT_DIR / "businesses_raw.json"
    FILE_BUSINESSES_JSON = BASE_OUTPUT_DIR / "businesses.json"
    FILE_BUSINESSES_FILTERED = BASE_OUTPUT_DIR / "businesses_filtered.json"
    FILE_BUSINESSES_WITH_IMAGES = BASE_OUTPUT_DIR / "businesses_final_image.json"
    FILE_IMAGE_JSON = BASE_OUTPUT_DIR / "images.json"
    FILE_PRE_NEW_POSTS_JSON = BASE_OUTPUT_DIR / "posts_pre_new.json"
    DB_FILENAME = BASE_OUTPUT_DIR / "blog.db"

    main()

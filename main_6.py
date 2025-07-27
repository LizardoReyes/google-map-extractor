"""
    SCRIPT para recuperar negocios ya existentes en WordPress como Pages.json
"""
import json
import os
import re
from pathlib import Path


from converts.convert_json_to_csv import convert_json_to_csv
from converts.convert_json_to_sqlite import convert_json_to_sqlite
from enums.Language import Language
from helpers.helpers_wordpress import reemplazar_su_gmap_por_iframe, centrar_h4_ul_enlinea, limpiar_html_basico, \
    limpiar_adinserter_y_img, convertir_etiquetas_p_b_minuscula, filtrar_json_por_slugs
from partials.categorize_businesses import generate_categories_from_posts_json
from partials.generate_images_json_and_names import generate_images_json_and_names
from partials.helper_csv import merge_json_in_folder, read_json_full, filter_businesses, \
    save_business
from partials.helpers import create_business, delete_files


def main():

    # Leemos un archivo JSON, creamos objetos Business y guardamos en un nuevo archivo JSON
    raw_data = read_json_full(ruta_archivo=FILE_WP_POSTS_JSON)
    pages = raw_data[2]["data"]
    print(f"Total de páginas encontradas: {len(pages)}")

    # Recorremos los datos y buscamos unas palabras y eliminamos la palabra esa
    for post in pages:
        content = post["content"]

        content = reemplazar_su_gmap_por_iframe(content)
        content = centrar_h4_ul_enlinea(content)

        # Limpieza de estructura básica
        content, _ = limpiar_html_basico(content, post_id=post["id"], post_title=post["title"])

        # Limpieza de adinserter e imágenes
        content, _ = limpiar_adinserter_y_img(content, post_id=post["id"], post_title=post["title"])

        # Aplicar conversión de etiquetas a minúscula
        content, _ = convertir_etiquetas_p_b_minuscula(content, post_id=post["id"], post_title=post["title"])

        # Limpieza de estructura básica
        content, _ = limpiar_html_basico(content, post_id=post["id"], post_title=post["title"])

        # Actualizamos el contenido del post
        post["content"] = content


    # Guardamos los datos de las páginas en un nuevo archivo JSON
    with open(FILE_PAGES_JSON, "w", encoding="utf-8") as file:
        json.dump(pages, file, ensure_ascii=False, indent=2)

    # Filtramos las páginas por los slugs del archivo slugs.txt
    filtrar_json_por_slugs(
        file_txt_slugs=FILE_SLUGS_TXT,
        file_json_entrada=FILE_PAGES_JSON,
        file_json_salida=FILE_PAGES_JSON
    )

    # Creamos la version en CSV
    convert_json_to_csv(json_path=FILE_PAGES_JSON, csv_path=FILE_PAGES_CSV)


if __name__ == "__main__":

    #############################
    # Nombre del archivo JSON de WordPress
    FILE_NAME = "p.json"
    #############################

    # Carpetas
    BASE_DIR = Path(__file__).resolve().parent
    BASE_INTPUT_DIR = BASE_DIR / "input"
    BASE_OUTPUT_DIR = BASE_DIR / "output"

    # Categorías y posts
    FILE_SLUGS_TXT = BASE_INTPUT_DIR / "slugs.txt"
    FILE_WP_POSTS_JSON = BASE_INTPUT_DIR / FILE_NAME
    FILE_PAGES_JSON = BASE_OUTPUT_DIR / "pages.json"
    FILE_PAGES_CSV = BASE_OUTPUT_DIR / "pages.csv"

    main()

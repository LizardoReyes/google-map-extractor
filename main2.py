import os

from helpers.verificar_imagenes_faltantes import verificar_imagenes_faltantes
from partials.categorize_businesses import generate_categories_from_posts
from partials.download_images import procesar_imagenes_csv, descargar_imagenes_validadas
from partials.generar_images_csv_y_nombres import generar_images_csv_y_nombres
from partials.helper_csv import unir_json_de_carpeta, leer_json_completo, guardar_csv, filtrar_negocios
from partials.helpers import create_business

#imprimir_datos_json(datos)
#print(datos[0]["about"][0]["options"][0]["enabled"])
#business = Business(datos[0])
#print(type(business.competitors))
#print(business.owner.id)
#print(business.review_keywords[0].keyword)
#print(business.reviews_per_rating["1"])
#print(type(business.reviews_per_rating["1"]))
#print(business.featured_question.answered_by.name)
#print(business.coordinates.latitude)
#print(business.detailed_address.city)
#print(business.about[0].options[0].name)
#print(business.images[0].link)
#print(business.hours[0].day)
#print(business.hours[0].times[0])
#print(business.most_popular_times[0].average_popularity)
#print(business.popular_times["Friday"][1].time_label)
#print(business.menu.source)
#print(business.reservations[0].link)
#print(business.order_online_links[0].link)
#print(business.featured_reviews[0].review_id)
#print(business.featured_reviews[0].experience_details[0].value)
#print(business.featured_reviews[0].review_photos[0].url)
#print(business.detailed_reviews)
#print(business.query)

# Unir los archivos JSON de la carpeta "businesses" y guardarlos en "businesses.json"

FOLDER_BUSINESSES = "businesses"
FILENAME_JSON = "businesses.json"
FILENAME_CSV = "businesses.csv"
FILENAME_CSV_FILTERED = "businesses_filtered.csv"
FILENAME_CSV_FILTERED_CATEGORIZED = "businesses_final.csv"
FILENAME_CSV_FILTERED_CATEGORIZED_IMAGE = "businesses_final_image.csv"
FILENAME_CATEGORIES = "categories.csv"
FILENAME_POSTS = "posts.csv"
CARPETA_IMAGES = "images"

# Unir los archivos JSON de la carpeta "businesses" y guardarlos en un unico archivo JSON
#unir_json_de_carpeta(carpeta=FOLDER_BUSINESSES, ruta_salida=FILENAME_JSON)

# Leer un archivo JSON desde una ruta específica
#raw_data = leer_json_completo(ruta_archivo=FILENAME_JSON)

# Crear una lista de objetos Business a partir de un JSON complejo
#business = create_business(raw_data)

# Guardar los datos de los negocios en un archivo CSV
#guardar_csv(negocios=business, ruta_salida=FILENAME_CSV)

# Filtramos los negocios por ciertas condiciones
#filtrar_negocios(nombre_archivo_csv=FILENAME_CSV, ruta_salida=FILENAME_CSV_FILTERED)

# Generamos las categorías a partir de los posts y guardamos en un nuevo archivo CSV
#generate_categories_from_posts(posts_file=FILENAME_CSV_FILTERED, output_posts_file=FILENAME_CSV_FILTERED_CATEGORIZED, categories_file=FILENAME_CATEGORIES)

# Procesar las imágenes desde el CSV filtrado y categorizado
###procesar_imagenes_csv(name_csv=FILENAME_CSV_FILTERED_CATEGORIZED, images_dir=CARPETA_IMAGES)
###descargar_imagenes_validadas(name_csv=FILENAME_CSV_FILTERED_CATEGORIZED, images_dir=CARPETA_IMAGES)

# Agregamos el campo imagen a los negocios en el CSV filtrado y categorizado
#generar_images_csv_y_nombres(nombre_csv=FILENAME_CSV_FILTERED_CATEGORIZED, output_csv=FILENAME_CSV_FILTERED_CATEGORIZED_IMAGE)

# Eliminamos los archivos temporales de negocios
#os.remove(FILENAME_JSON)
#os.remove(FILENAME_CSV)
#os.remove(FILENAME_CSV_FILTERED)
#os.remove(FILENAME_CSV_FILTERED_CATEGORIZED)
#os.rename(FILENAME_CSV_FILTERED_CATEGORIZED_IMAGE, FILENAME_POSTS)

# Verificamos si faltan imagenes por descargar
verificar_imagenes_faltantes(csv_path="images.csv", carpeta_imagenes=CARPETA_IMAGES, salida_csv="images_faltantes.csv")
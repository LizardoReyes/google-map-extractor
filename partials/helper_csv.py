import csv
import json
import os
import pandas as pd

from models.Business import Business
from partials.helpers import obtener_dominio_base, create_content, obtener_horario, slugify


def unir_json_de_carpeta(carpeta, ruta_salida):
    datos_unidos = []

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".json"):
            ruta = os.path.join(carpeta, archivo)
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = json.load(f)
                if isinstance(contenido, list):
                    datos_unidos.extend(contenido)
                else:
                    datos_unidos.append(contenido)

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(datos_unidos, f, ensure_ascii=False, indent=2)

    print(f"✅ Combinados {len(datos_unidos)} registros en: {ruta_salida}")

def unir_csv_en_carpeta(carpeta, salida):
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".csv")]
    encabezado_escrito = False

    with open(salida, 'w', newline='', encoding='utf-8') as archivo_salida:
        writer = None

        for archivo in archivos:
            ruta = os.path.join(carpeta, archivo)
            with open(ruta, 'r', encoding='utf-8') as archivo_entrada:
                reader = csv.reader(archivo_entrada)
                encabezado = next(reader)

                if not encabezado_escrito:
                    writer = csv.writer(archivo_salida)
                    writer.writerow(encabezado)
                    encabezado_escrito = True

                for fila in reader:
                    writer.writerow(fila)

    print(f"✅ Archivos combinados en: {salida}")

def unir_csv_y_exportar_json(carpeta_csv, archivo_salida_json):
    datos = []

    archivos = [f for f in os.listdir(carpeta_csv) if f.endswith('.csv')]

    for archivo in archivos:
        ruta = os.path.join(carpeta_csv, archivo)
        with open(ruta, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)  # usa encabezados como claves
            for fila in reader:
                datos.append(fila)

    with open(archivo_salida_json, 'w', encoding='utf-8') as salida:
        json.dump(datos, salida, ensure_ascii=False, indent=2)

    print(f"✅ Exportados {len(datos)} registros a {archivo_salida_json}")

def leer_json_completo(ruta_archivo):
    """
    Lee un archivo JSON con estructura de lista de diccionarios complejos
    y devuelve su contenido como un objeto Python.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)
    return data

def imprimir_datos_json(data):
    """
    Recorre e imprime todos los campos de cada objeto en el JSON, incluyendo estructuras anidadas.
    """
    def imprimir_recursivo(obj, indent=0):
        espacio = '  ' * indent
        if isinstance(obj, dict):
            for clave, valor in obj.items():
                print(f"{espacio}{clave}:")
                imprimir_recursivo(valor, indent + 1)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                print(f"{espacio}- [{i}]")
                imprimir_recursivo(item, indent + 1)
        else:
            print(f"{espacio}{obj}")

    for i, item in enumerate(data):
        print(f"\n===== Restaurante {i + 1} =====")
        imprimir_recursivo(item)

def guardar_csv(negocios: list[Business], ruta_salida: str):
    with (open(ruta_salida, mode='w', newline='', encoding='utf-8') as archivo):
        writer = csv.writer(archivo)

        # Escribir encabezado
        writer.writerow(['title', 'slug', 'rating', 'reviews', 'reviews_link', 'web_url', 'web_url_root', 'phone', 'image_1', 'image_2', 'image_3', 'categories', 'address', 'google_maps_url' , 'price_range', 'zipcode', 'city', 'state', 'hoary', 'link_menu', 'link_reservations', 'link_order_online', 'content'])

        # Escribir datos de cada negocio
        for negocio in negocios:
            title = negocio.name
            slug = slugify(title)
            rating = negocio.rating
            reviews = negocio.reviews
            reviews_link = negocio.reviews_link
            web_url = negocio.website if negocio.website else negocio.reviews_link
            web_url_root = obtener_dominio_base(web_url)
            phone = negocio.phone or "N/A"
            image_1 = negocio.featured_image if negocio.featured_image else None
            image_2 = negocio.images[0].link if negocio.images else None
            image_3 = negocio.images[1].link if len(negocio.images) > 1 else None
            categories = ", ".join(negocio.categories).lower() if negocio.categories else "N/A"
            address = negocio.address
            google_maps = negocio.link
            price_range = negocio.price_range
            zipcode = negocio.detailed_address.postal_code if negocio.detailed_address else "N/A"
            state = negocio.detailed_address.state if negocio.detailed_address.state else "N/A"
            city = negocio.detailed_address.city if negocio.detailed_address.city else state
            horary = obtener_horario(negocio.hours)
            link_menu = negocio.menu.link if negocio.menu else None
            link_reservations = negocio.reservations[0].link if negocio.reservations else None
            link_order_online = negocio.order_online_links[0].link if negocio.order_online_links else None
            content = create_content(
                title=title, address=address, phone=phone, rating=rating, reviews=reviews, web_url=web_url, categories=categories, price_range=price_range, zipcode=zipcode, city=city,
            )

            writer.writerow([
                title,
                slug,
                rating,
                reviews,
                reviews_link,
                web_url,
                web_url_root,
                phone,
                image_1,
                image_2,
                image_3,
                categories,
                address,
                google_maps,
                price_range,
                zipcode,
                city,
                state,
                horary,
                link_menu,
                link_reservations,
                link_order_online,
                content,
            ])

    print(f"✅ Datos guardados en: {ruta_salida} ({len(negocios)} negocios)")


def filtrar_negocios(nombre_archivo_csv, ruta_salida="negocios_filtrados.csv"):

    # Leer archivo original sin convertir "N/A" en NaN
    df = pd.read_csv(nombre_archivo_csv, keep_default_na=False, na_values=[])

    # Limpiar espacios por si acaso
    df['slug'] = df['slug'].astype(str).str.strip()

    # Eliminar duplicados por slug directamente
    df = df.drop_duplicates(subset=['slug'])

    # Convertir rating y reviews a numéricos
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')

    # Filtrar por condiciones de calidad
    df_filtrado = df[(df['rating'] >= 3.5) & (df['reviews'] >= 5)].copy()

    # Agregar ID autoincremental
    df_filtrado.insert(0, 'id', range(1, len(df_filtrado) + 1))

    # Guardar CSV limpio
    df_filtrado.to_csv(ruta_salida, index=False)
    print(f"✅ Filtrado a {len(df_filtrado)} negocios con ID autogenerado en '{ruta_salida}'.")



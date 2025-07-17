import csv
import json
import os
from pathlib import Path

import pandas as pd

from models.Business import Business
from enums.Language import Language
from partials.helpers import get_base_domain, create_content, get_translated_schedule, slugify

def read_csv(csv_path: Path, *, fallback_engine: str = "python", dtype_backend: str = "pyarrow") -> pd.DataFrame:
    """
    Intenta leer un CSV usando PyArrow para mayor eficiencia, y hace fallback automático si falla.

    Args:
        csv_path (Path): Ruta al archivo CSV.
        fallback_engine (str): Motor a usar si falla PyArrow (por defecto "python").
        dtype_backend (str): Backend de tipos de datos (por defecto "pyarrow").

    Returns:
        pd.DataFrame: DataFrame resultante.
    """
    try:
        return pd.read_csv(csv_path, engine="pyarrow", dtype_backend=dtype_backend)
    except Exception as e:
        print(f"⚠️ Fallback a engine='{fallback_engine}' por error en PyArrow: {e}")
        return pd.read_csv(csv_path, engine=fallback_engine)


def merge_json_in_folder(carpeta: Path, ruta_salida: Path) -> None:
    datos_unidos = []

    for archivo in carpeta.iterdir():
        if archivo.suffix == ".json" and archivo.is_file():
            with archivo.open('r', encoding='utf-8') as f:
                contenido = json.load(f)
                if isinstance(contenido, list):
                    datos_unidos.extend(contenido)
                else:
                    datos_unidos.append(contenido)

    with ruta_salida.open('w', encoding='utf-8') as f:
        json.dump(datos_unidos, f, ensure_ascii=False, indent=2)

    print(f"✅ Combinados {len(datos_unidos)} registros en: {ruta_salida.name}")


def merge_csv_in_folder(carpeta: Path, salida: Path):
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


def join_csv_and_export_json(carpeta_csv: Path, archivo_salida_json: Path):
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


def read_json_full(ruta_archivo: Path):
    """
    Lee un archivo JSON con estructura de lista de diccionarios complejos
    y devuelve su contenido como un objeto Python.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)
    return data


def read_csv_full(ruta_archivo: Path):
    """
    Lee un archivo CSV y devuelve su contenido como un DataFrame de pandas.
    Utiliza PyArrow para mayor eficiencia, con fallback a engine='python' si falla.
    """
    try:
        df = pd.read_csv(ruta_archivo, engine="pyarrow", dtype_backend="pyarrow")
    except Exception as e:
        print(f"⚠️ Fallback a engine='python' por error en PyArrow: {e}")
        df = pd.read_csv(ruta_archivo, engine="python")
    return df


def print_json_data(data):
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
            for ii, item1 in enumerate(obj):
                print(f"{espacio}- [{ii}]")
                imprimir_recursivo(item1, indent + 1)
        else:
            print(f"{espacio}{obj}")

    for i, item in enumerate(data):
        print(f"\n===== Restaurante {i + 1} =====")
        imprimir_recursivo(item)


def save_business(business: list[Business], ruta_salida: Path, lang: Language = Language.EN) -> None:
    datos_json = []

    for negocio in business:
        title = negocio.name
        slug = slugify(title)
        rating = negocio.rating
        reviews = negocio.reviews
        reviews_link = negocio.reviews_link
        web_url = negocio.website or reviews_link
        web_url_root = get_base_domain(web_url)
        phone = negocio.phone
        image_1 = negocio.featured_image or None
        image_2 = negocio.images[0].link if negocio.images else None
        image_3 = negocio.images[1].link if len(negocio.images) > 1 else None
        categories = ", ".join(negocio.categories).lower() if negocio.categories else "N/A"
        address = negocio.address
        google_maps = negocio.link
        price_range = negocio.price_range
        zipcode = negocio.detailed_address.postal_code if negocio.detailed_address else "N/A"
        state = negocio.detailed_address.state if negocio.detailed_address and negocio.detailed_address.state else "General"
        city = negocio.detailed_address.city if negocio.detailed_address and negocio.detailed_address.city else state
        hoary = get_translated_schedule(negocio.hours, lang)
        link_menu = negocio.menu.link if negocio.menu else None
        link_reservations = negocio.reservations[0].link if negocio.reservations else None
        link_order_online = negocio.order_online_links[0].link if negocio.order_online_links else None

        content = create_content(
            title=title,
            address=address,
            phone=phone,
            rating=rating,
            reviews=reviews,
            web_url=web_url,
            categories=categories,
            price_range=price_range,
            zipcode=zipcode,
            city=city,
            lang=lang,
        )

        datos_json.append({
            "title": title,
            "slug": slug,
            "rating": rating,
            "reviews": reviews,
            "reviews_link": reviews_link,
            "web_url": web_url,
            "web_url_root": web_url_root,
            "phone": phone,
            "image_1": image_1,
            "image_2": image_2,
            "image_3": image_3,
            "categories": categories,
            "address": address,
            "google_maps_url": google_maps,
            "price_range": price_range,
            "zipcode": zipcode,
            "city": city,
            "state": state,
            "hoary": hoary,
            "link_menu": link_menu,
            "link_reservations": link_reservations,
            "link_order_online": link_order_online,
            "content": content,
        })

    with ruta_salida.open('w', encoding='utf-8') as archivo:
        json.dump(datos_json, archivo, ensure_ascii=False, indent=2)

    print(f"✅ Datos guardados en: {ruta_salida.name} ({len(business)} negocios)")


def get_numbers_rows(nombre_archivo_json: Path):
    """
    Obtiene el número de filas en un archivo JSON que contiene una lista de diccionarios.

    Args:
        nombre_archivo_json (Path): Ruta al archivo JSON.

    Returns:
        int: Número de filas en el archivo JSON.
    """
    with open(nombre_archivo_json, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    return len(datos)


def filter_businesses(nombre_archivo_json: Path, ruta_salida: Path, id_inicio: int = 1,
                      min_rating: float = 3.5, min_reviews: int = 2) -> None:
    # Leer archivo JSON
    with open(nombre_archivo_json, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    df = pd.DataFrame(datos)

    # Limpiar espacios por si acaso
    df['slug'] = df['slug'].astype(str).str.strip()
    df['title'] = df['title'].astype(str).str.strip()

    # Eliminar duplicados por slug
    df = df.drop_duplicates(subset=['slug'])

    # Convertir columnas numéricas
    df['rating'] = pd.to_numeric(df.get('rating', 0), errors='coerce')
    df['reviews'] = pd.to_numeric(df.get('reviews', 0), errors='coerce')

    # Eliminar negocios sin título válido (title nulo o vacío)
    df = df[df['title'].notna() & (df['title'].str.lower() != 'none') & (df['title'].str.strip() != '')]

    # Filtrar negocios con suficientes reviews y rating
    filtro_validados = (df['rating'] >= min_rating) & (df['reviews'] >= min_reviews)

    # Filtrar negocios con 0 reviews pero al menos 1 dato útil
    filtro_nuevos_utiles = (df['reviews'] == 0) & (
        df['phone'].notna() | df['web_url'].notna() | df['image_1'].notna() | df['image_2'].notna() | df['image_3'].notna()
    )

    # Combinar ambos filtros
    df_filtrado = df[filtro_validados | filtro_nuevos_utiles].copy()

    # Agregar ID auto-incremental desde id_inicio
    df_filtrado.insert(0, 'id', range(id_inicio, id_inicio + len(df_filtrado)))

    # Limpiar campos de enlaces si existen
    if 'reviews_link' in df_filtrado.columns:
        df_filtrado['reviews_link'] = df_filtrado['reviews_link'].str.replace('&gl=PE', '', regex=False)
    if 'web_url' in df_filtrado.columns:
        df_filtrado['web_url'] = df_filtrado['web_url'].str.replace('&gl=PE', '', regex=False)

    # Guardar archivo JSON
    with open(ruta_salida, 'w', encoding='utf-8') as salida:
        json.dump(df_filtrado.to_dict(orient='records'), salida, ensure_ascii=False, indent=2)

    print(f"✅ Filtrado a {len(df_filtrado)} negocios con ID desde {id_inicio} en '{ruta_salida}'.")

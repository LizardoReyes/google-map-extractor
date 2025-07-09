import json
import random
import re
from pathlib import Path
from string import Template
from urllib.parse import urlparse

from models.Business import Business, Hour
from enums.Language import Language

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "unavailable_schedule_messages.json"

def create_business(data):
    return[Business(item) for item in data]


def get_base_domain(url):
    """
    Extrae el dominio base de una URL.
    :param url: URL de la que se extraerá el dominio.
    :return: Dominio base como cadena de texto.
    """
    parsed = urlparse(url)
    dominio = parsed.netloc  # Ej: 'pauseandplay.es' o 'www.decathlon.es'
    # Opcional: quitar 'www.' si está presente
    if dominio.startswith("www."):
        dominio = dominio[4:]
    return dominio


def get_schedule(hours: list[Hour], lang: Language = Language.EN) -> str:

    # Cargar el archivo correctamente
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        unavailable_messages = json.load(f)

    # Asegura que exista el idioma
    mensajes = unavailable_messages.get(lang.value, Language.EN.value)

    if len(hours) == 0:
        mensaje = random.choice(mensajes)
        return f"<p>{mensaje}</p>"

    html = "<ul>"
    for item in hours:
        day = item.day
        times = ", ".join(item.times)
        html += f'<li><b>{day}:</b> {times}</li>'
    html += "</ul>"
    return html


def extract_local_phone(phone: str):
    if not phone:
        return "N/A"

    # Elimina el + y los dígitos del código de país (1-3 dígitos), y espacios iniciales
    return re.sub(r"^\+\d{1,3}\s*", "", phone)


def create_content(title: str, address: str, phone: str, rating: str, web_url: str, reviews: str, categories: str, city: str, price_range: str, zipcode: str):

    plantilla_html = Template(
        "<p>$title is located at $address, in the city of $city with postal code $zipcode "
        "and offers quality products/services.</p><br/>"
        "<p>If you want, call $phone to learn about all the products and services they offer. "
        "It has a rating of $rating/5 based on $reviews reviews on its Google Maps listing.</p><br/>"
        "<p>It belongs to the $categories category. "
        "For more information, visit their website: <a href='$web_url' target='_blank' class='underline'>$web_url_root</a>.</p><br/>"
    )

    return plantilla_html.substitute(
        title=title,
        address=address,
        phone=extract_local_phone(phone),
        rating=rating,
        web_url=web_url,
        web_url_root=get_base_domain(web_url),
        reviews=reviews,
        categories=categories,
        city=city,
        price_range=price_range,
        zipcode=zipcode,
    )


def slugify(text: str) -> str:
    if not text:
        return ""

    text = text.lower()

    # Reemplaza todo tipo de espacios (incluye ideográficos, árabes, etc.) por guiones
    text = re.sub(r"\s+", "-", text, flags=re.UNICODE)

    # Reemplaza símbolos comunes
    text = text.replace("/", "-").replace("&", "-and-")

    # Elimina paréntesis, comillas, puntuación no alfabética
    text = re.sub(r"[\(\)\[\]\{\}<>«»“”\"']", "", text)

    # Elimina caracteres que NO son letras, números, guiones o caracteres CJK/árabes/coreanos
    text = re.sub(
        r"[^\w\-一-龯ぁ-んァ-ンーء-ي가-힣]",
        "",
        text
    )

    # Unifica guiones múltiples
    text = re.sub(r"-{2,}", "-", text)

    # Elimina guiones al inicio o fin
    text = text.strip("-")

    # Es posible que el texto sea muy grande, así que lo acorta a 20 caracteres
    if len(text) > 20:
        text = text[:20]

    # Es posible que el texto ya esté vacío después de las transformaciones, entonces randomiza un texto por defecto
    if not text:
        return "business" + str(random.randint(1, 9999))

    return text


def delete_files(files: list[Path]) -> None:
    """
    Elimina los archivos especificados en la lista.
    :param files: Lista de rutas de archivos a eliminar.
    """
    for file in files:
        try:
            if file.exists():
                file.unlink()
                #print(f"✅ Archivo eliminado: {file}")
            else:
                print(f"⚠️ El archivo no existe: {file}")
        except Exception as e:
            print(f"❌ Error al eliminar el archivo {file}: {e}")

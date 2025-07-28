import json
import random
import re
from pathlib import Path
from string import Template
from urllib.parse import urlparse

from models.Business import Business, Hour
from enums.Language import Language
from models.Business2 import Business2

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH_UNAVAILABLE_SCHEDULE_MSGS = BASE_DIR / "unavailable_schedule_messages.json"
JSON_PATH_AVAILABLE_REVIEWS_MSGS = BASE_DIR / "available_reviews_messages.json"
JSON_PATH_UNAVAILABLE_REVIEWS_MSG = BASE_DIR / "unavailable_reviews_messages.json"
JSON_PATH_BASE_CONTENT_MSGS = BASE_DIR / "base_content_messages.json"

def create_business(data):
    return[Business(item) for item in data]


def create_bussiness_2(data):
    return [Business2(item) for item in data]


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


def get_generic_message(json_file: Path, language: Language = Language.EN) -> str:

    # Cargar el archivo JSON con los mensajes
    with open(json_file, "r", encoding="utf-8") as f:
        messages = json.load(f)

    options = messages.get(language.value) or messages.get(Language.EN.value, [])
    if not options:
        raise ValueError(f"No messages found for language '{language.value}' in {json_file}")

    return random.choice(options)


def get_translated_schedule(hours: list[Hour], lang: Language = Language.EN) -> str:

    if len(hours) == 0:
        message = get_generic_message(JSON_PATH_UNAVAILABLE_SCHEDULE_MSGS, lang)
        return f"<p>{message}</p>"

    html = "<ul>"
    for item in hours:
        day = item.day
        times = ", ".join(item.times)
        html += f'<li><b>{day}:</b> {times}</li>'
    html += "</ul>"
    return html


def get_translated_schedule_2(hours: dict, lang: Language = Language.EN) -> str:
    if not hours:
        message = get_generic_message(JSON_PATH_UNAVAILABLE_SCHEDULE_MSGS, lang)
        return f"<p>{message}</p>"

    html = "<ul>"
    for day, times in hours.items():
        html += f'<li><b>{day.capitalize()}:</b> {times}</li>'
    html += "</ul>"
    return html


def create_content(title: str, address: str, phone: str, rating: str, web_url: str,
                   reviews: str, categories: str, city: str, price_range: str, zipcode: str, lang: Language = Language.EN) -> str:

    # Construir texto condicional de reseñas
    try:
        reviews_num = int(reviews)
    except (ValueError, TypeError):
        reviews_num = 0  # Si es nulo o no convertible

    if reviews_num > 0:
        reviews_text = get_generic_message(JSON_PATH_AVAILABLE_REVIEWS_MSGS, lang).format(reviews=reviews_num, rating=rating)
    else:
        reviews_text = get_generic_message(JSON_PATH_UNAVAILABLE_REVIEWS_MSG, lang)

    plantilla_html = Template(get_generic_message(JSON_PATH_BASE_CONTENT_MSGS, lang))

    return plantilla_html.substitute(
            title=title,
            address=address,
            phone=extract_local_phone(phone),
            rating=rating,
            web_url=web_url,
            web_url_root=get_base_domain(web_url),
            reviews_text=reviews_text,
            categories=categories,
            city=city,
            price_range=price_range,
            zipcode=zipcode,
        )


def extract_local_phone(phone: str):
    if not phone:
        return "N/A"

    # Elimina el + y los dígitos del código de país (1-3 dígitos), y espacios iniciales
    return re.sub(r"^\+\d{1,3}\s*", "", phone)



def slugify(text: str) -> str:
    if not text:
        return ""

    # 🔤 Mapa de conversión de letras negrita Unicode a ASCII normal
    bold_map = str.maketrans(
        "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"
        "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙",
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    text = text.translate(bold_map)

    text = text.lower()

    # Reemplaza espacios por guiones
    text = re.sub(r"\s+", "-", text, flags=re.UNICODE)

    # Reemplaza símbolos comunes
    text = text.replace("/", "-").replace("&", "-and-")

    # Elimina paréntesis, comillas y puntuación no alfabética
    text = re.sub(r"[\(\)\[\]\{\}<>«»“”\"']", "", text)

    # Mantiene letras, números, guiones y letras CJK/árabes/coreanos
    text = re.sub(r"[^\w\-一-龯ぁ-んァ-ンーء-ي가-힣]", "", text)

    # Unifica guiones múltiples
    text = re.sub(r"-{2,}", "-", text)

    # Elimina guiones al inicio o final
    text = text.strip("-")

    # Limita a 20 caracteres
    if len(text) > 20:
        text = text[:20]

    # Si queda vacío, asigna uno genérico
    if not text:
        return "business" + str(random.randint(1, 99))

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

import os
import random
import re
from pathlib import Path
from string import Template
from urllib.parse import urlparse

from models.Business import Business, Hour


def create_business(data):
    return[Business(item) for item in data]

def obtener_dominio_base(url):
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

def obtener_horario(hours: list[Hour]) -> str:
    unavailableScheduleMessage = [
    "No se dispone de la información sobre los horarios de atención.",
    "La franja horaria de operación no ha sido especificada.",
    "Los momentos de atención al cliente no están definidos.",
    "Aún no se han proporcionado los detalles sobre los horarios disponibles.",
    "La empresa no ha divulgado la información relativa a sus horarios.",
    "La disponibilidad de atención al público no ha sido especificada.",
    "Se carece de detalles acerca de los periodos de atención.",
    "La información sobre los horarios de servicio está pendiente.",
    "No se cuenta con datos precisos sobre los momentos de funcionamiento.",
    "Los horarios de atención al cliente son desconocidos en este momento.",
    "La franja temporal para consultas aún no ha sido establecida.",
    "No se tiene conocimiento acerca de las horas de servicio.",
    "Los periodos de atención y disponibilidad no han sido comunicados.",
    "La empresa aún no ha compartido detalles sobre sus horarios laborales.",
    "Los momentos específicos para la atención al cliente no han sido revelados.",
    "No se dispone de información precisa sobre los tiempos de operación.",
    "La empresa no ha especificado los horarios de atención al público.",
    "La información sobre los horarios de trabajo aún no ha sido publicada.",
    "Se desconoce la franja horaria en la que la empresa está disponible.",
    "Los detalles sobre los horarios de funcionamiento están por determinarse.",
    "La empresa no ha proporcionado información sobre las horas de atención.",
    "No se cuenta con datos disponibles sobre los momentos de servicio.",
    "La información sobre los horarios laborales aún no ha sido divulgada.",
    "Los periodos de atención al cliente se encuentran sin determinar.",
    "Se desconoce actualmente la disponibilidad horaria de la empresa.",
    "No se tienen detalles específicos sobre los horarios de atención.",
    "La empresa aún no ha comunicado la hora de inicio y finalización.",
    "No se dispone de información precisa sobre las horas de operación.",
    "La franja temporal para consultas y servicios está por confirmar.",
    "Los detalles relativos a los horarios de servicio aún no han sido compartidos.",
    "No se cuenta con información detallada sobre los momentos de atención.",
    "La empresa no ha establecido de manera clara sus horarios laborales.",
    "Se desconoce la disponibilidad horaria para actividades específicas.",
    "Los horarios de atención al público aún no han sido especificados.",
    "No se tiene constancia de los periodos de operación de la empresa.",
    "La información sobre los horarios de atención al cliente está en espera.",
    "La empresa no ha divulgado detalles sobre sus horas de servicio.",
    "Los momentos específicos de atención al público no se han revelado.",
    "No se dispone de datos concretos sobre la franja horaria de operación.",
    "La hora de inicio y finalización de operaciones aún no ha sido comunicada.",
    "Los horarios de servicio no han sido establecidos con claridad.",
    "La disponibilidad de atención al cliente no ha sido especificada.",
    "Se desconoce actualmente la hora de inicio y cierre de actividades.",
    "No se cuenta con detalles sobre los horarios de operación de la empresa.",
    "La información sobre los momentos de atención aún no está disponible.",
    "Los horarios laborales de la empresa se mantienen sin determinar.",
    "No se dispone de datos concretos sobre la disponibilidad horaria.",
    "La empresa aún no ha compartido detalles sobre sus horas de atención.",
    "Los periodos específicos de funcionamiento no han sido especificados.",
    "Se desconoce actualmente la hora de operación de la empresa."
]

    if len(hours) == 0:
        return "<p>" + unavailableScheduleMessage[random.randint(0, len(unavailableScheduleMessage) - 1)] + "</p>"

    html = "<ul>\n"
    for item in hours:
        day = item.day
        times = ", ".join(item.times)
        html += f'  <li><b>{day}:</b> {times}</li>\n'
    html += "</ul>"
    return html

def extract_local_phone(phone: str):
    if not phone:
        return "N/A"

    # Elimina el + y los dígitos del código de país (1-3 dígitos), y espacios iniciales
    return re.sub(r"^\+\d{1,3}\s*", "", phone)

def create_content(title: str, address: str, phone: str, rating: str, web_url: str, reviews: str, categories: str, city: str, price_range: str, zipcode: str):

    plantilla_html = Template(
        "<p>$title está ubicada en $address, en la ciudad de $city con código postal $zipcode "
        "y ofrece productos/servicios de calidad.</p><br/>"
        "<p>Si quieres, llama al $phone para ver todos los productos y servicios que pueden ofrecer. "
        "Tiene una calificación de $rating/5 con $reviews votos en su ficha de Google Maps.</p><br/>"
        "<p>Está en la categoría de $categories. "
        "Para más información, visita su página web: <a href='$web_url' target='_blank' class='underline'>$web_url_root</a>.</p><br/>"
    )

    return plantilla_html.substitute(
        title=title,
        address=address,
        phone=extract_local_phone(phone),
        rating=rating,
        web_url=web_url,
        web_url_root=obtener_dominio_base(web_url),
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
        return "business-" + str(random.randint(1, 9999))

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
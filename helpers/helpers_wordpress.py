import json
import re

from pathlib import Path
from urllib.parse import quote

def reemplazar_su_gmap_por_iframe(content):
    pattern = r'\[su_gmap[^\]]*?address="(.*?)"[^\]]*\]'

    def replacer(match):
        address = match.group(1)
        encoded_address = quote(address)
        iframe = (
            f'<iframe class="w-full max-w-[500px] h-72 rounded"'
            f' src="https://maps.google.com/maps?width=100%25&height=400&q={encoded_address}&t=&z=14&ie=UTF8&iwloc=B&output=embed"'
            f' loading="lazy"></iframe>'
        )
        return iframe

    nuevo_contenido, cantidad = re.subn(pattern, replacer, content)
    return nuevo_contenido


def centrar_h4_ul_enlinea(content):
    def agregar_style_centrado(match):
        tag = match.group(1).lower()        # h4 o ul
        attrs = match.group(2) or ""        # atributos existentes
        resto = match.group(3)              # lo que sigue

        # Determinar el style a agregar
        if tag == "h4":
            extra_style = "text-align: center; font-weight: bold;"
        else:  # ul
            extra_style = "text-align: center;"

        if 'style=' in attrs:
            # Añadir el nuevo estilo al final del style existente
            nuevo_attrs = re.sub(
                r'style\s*=\s*["\'](.*?)["\']',
                lambda m: f'style="{m.group(1).rstrip(";")}; {extra_style}"',
                attrs,
                flags=re.IGNORECASE
            )
        else:
            nuevo_attrs = f'{attrs} style="{extra_style}"'

        return f'<{tag}{nuevo_attrs}>{resto}'

    # Patrón que captura: <h4 ...> y <ul ...> incluyendo atributos opcionales
    pattern = r'<(h4|ul)([^>]*)>(.*?)'

    nuevo_contenido, cantidad = re.subn(
        pattern,
        agregar_style_centrado,
        content,
        flags=re.IGNORECASE | re.DOTALL
    )

    return nuevo_contenido


def limpiar_html_basico(content: str, post_id=None, post_title=None):
    cambios = False

    if '<div class="responsive-two-columns">\r\n' in content:
        content = content.replace('<div class="responsive-two-columns">\r\n', "")
        cambios = True

    nuevo_contenido, cantidad = re.subn(
        r'</a></center></div>\s*</div>',
        '</a></center></div>',
        content,
        flags=re.IGNORECASE
    )
    if cantidad > 0:
        content = nuevo_contenido
        cambios = True

    if "\r\n\r\n" in content:
        content = content.replace("\r\n\r\n", "<br/>")
        cambios = True

    if "\r\n" in content:
        content = content.replace("\r\n", "<br/>")
        cambios = True

    if "<div><br/>" in content:
        content = content.replace("<div><br/>", "<div>")
        cambios = True

    if "<br/><br/><br/>" in content:
        content = content.replace("<br/><br/><br/>", "<br/>")
        cambios = True

    return content, cambios


def limpiar_adinserter_y_img(content, post_id=None, post_title=None):
    cambios = False

    if '[adinserter block="1"]' in content:
        content = content.replace('[adinserter block="1"]', "")
        cambios = True

    if '[adinserter block="2"]' in content:
        content = content.replace('[adinserter block="2"]', "")
        cambios = True

    nuevo_contenido, cantidad = re.subn(r"<img[^>]*>", "", content, flags=re.IGNORECASE)
    if cantidad > 0:
        content = nuevo_contenido
        cambios = True

    return content, cambios


def convertir_etiquetas_p_b_minuscula(content, post_id=None, post_title=None):
    # Patrón que detecta <P>, </P>, <B>, </B> con mayúsculas
    pattern = r"</?P>|</?B>"

    def replacer(match):
        return match.group(0).lower()

    nuevo_contenido, cantidad = re.subn(pattern, replacer, content)

    return nuevo_contenido, cantidad > 0


def filtrar_json_por_slugs(file_txt_slugs: Path, file_json_entrada: Path, file_json_salida: Path):
    slugs = set()

    # Verificar si el archivo TXT existe y leer slugs
    if file_txt_slugs.exists():
        with file_txt_slugs.open(encoding="utf-8") as f:
            for line in f:
                slug = line.strip()
                if slug:
                    slugs.add(slug)
        print(f"Total slugs cargados: {len(slugs)}")
    else:
        print(f"No se encontró {file_txt_slugs}, NO se filtrará ni guardará nada.")
        return

    # Leer el JSON de entrada
    with file_json_entrada.open(encoding="utf-8") as f:
        data = json.load(f)

    # Filtrar si hay slugs, sino mantener todo
    if slugs:
        filtrados = [item for item in data if "slug" in item and item["slug"] in slugs]
        print(f"Total items filtrados: {len(filtrados)} de {len(data)}")
    else:
        print("Archivo de slugs vacío, NO se filtrará, se mantendrán todos los elementos.")
        filtrados = data

    # Reiniciar IDs siempre si hay elementos
    if filtrados:
        for idx, item in enumerate(filtrados, start=1):
            item["id"] = idx

        with file_json_salida.open("w", encoding="utf-8") as f:
            json.dump(filtrados, f, ensure_ascii=False, indent=2)
        print(f"Archivo final con IDs reiniciados guardado en: {file_json_salida.resolve()}")
    else:
        print("No se encontraron coincidencias de slugs, NO se generó archivo de salida.")
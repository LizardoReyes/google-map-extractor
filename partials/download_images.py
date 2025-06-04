import csv
import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse
from partials.helpers import slugify  # Asegúrate de tener esta función


# 🔧 Headers para simular navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com"
}


def verificar_url_imagen(url: str) -> bool:
    try:
        response = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False


def generar_nombre_imagen(title: str, contador: int, url: str) -> str:
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"
    return f"{slugify(title)}-{contador}{ext}"


def procesar_imagenes_csv(name_csv: str, images_dir: str = "images") -> None:
    BASE_DIR = Path(__file__).resolve().parent
    IMAGES_DIR = BASE_DIR.parent / images_dir
    os.makedirs(IMAGES_DIR, exist_ok=True)

    with open(name_csv, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        fieldnames = list(reader[0].keys())

    if "image" not in fieldnames:
        fieldnames.append("image")
        for row in reader:
            row["image"] = ""

    existing_images = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(IMAGES_DIR / f)]
    used_numbers = [
        int(re.search(r"-(\d+)\.", f).group(1))
        for f in existing_images if re.search(r"-(\d+)\.", f)
    ]
    image_counter = max(used_numbers) + 1 if used_numbers else 1

    total = len(reader)
    asignadas = 0

    with open(name_csv, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for idx, row in enumerate(reader, start=1):
            if row.get("image"):
                writer.writerow(row)
                continue

            title = row.get("title", "").strip()
            intentos = []
            nombre_imagen = ""
            imagen_valida = False

            for key in ["image_1", "image_2", "image_3"]:
                url = row.get(key, "").strip()
                intentos.append(url)

                if not url:
                    continue

                nombre_temp = generar_nombre_imagen(title, image_counter, url)
                ruta_destino = IMAGES_DIR / nombre_temp

                if ruta_destino.exists():
                    row["image"] = nombre_temp
                    asignadas += 1
                    print(f"{idx}/{total} 🟡 Ya existe localmente: {nombre_temp}")
                    imagen_valida = True
                    break

                if verificar_url_imagen(url):
                    row["image"] = nombre_temp
                    image_counter += 1
                    asignadas += 1
                    print(f"{idx}/{total} ✅ URL válida: {nombre_temp}")
                    imagen_valida = True
                    break

            if not imagen_valida:
                row["image"] = ""
                print(f"{idx}/{total} ❌ Ninguna imagen válida. URLs:")
                for u in intentos:
                    print(f"   - {u}")

            writer.writerow(row)

    print(f"\n✅ Validación terminada: {asignadas} imágenes asignadas o confirmadas localmente.")


def descargar_imagenes_validadas(name_csv: str, images_dir: str = "images") -> None:
    BASE_DIR = Path(__file__).resolve().parent
    IMAGES_DIR = BASE_DIR.parent / images_dir
    os.makedirs(IMAGES_DIR, exist_ok=True)

    with open(name_csv, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        total = len(reader)
        descargadas = 0

        for idx, row in enumerate(reader, start=1):
            nombre_imagen = row.get("image", "").strip()
            if not nombre_imagen:
                continue

            ruta_destino = IMAGES_DIR / nombre_imagen
            if ruta_destino.exists():
                print(f"{idx}/{total} 🟡 Ya descargada: {nombre_imagen}")
                continue

            url_asignada = None
            for key in ["image_1", "image_2", "image_3"]:
                url = row.get(key, "").strip()
                if url and nombre_imagen in url:
                    url_asignada = url
                    break

            if not url_asignada:
                for key in ["image_1", "image_2", "image_3"]:
                    url = row.get(key, "").strip()
                    if url:
                        url_asignada = url
                        break

            if not url_asignada:
                print(f"{idx}/{total} ❌ Sin URL válida para descargar: {nombre_imagen}")
                continue

            try:
                response = requests.get(url_asignada, headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    with open(ruta_destino, "wb") as img_file:
                        img_file.write(response.content)
                    descargadas += 1
                    print(f"{idx}/{total} ✅ Descargada: {nombre_imagen}")
                else:
                    print(f"{idx}/{total} ⚠️ Error HTTP {response.status_code} → {url_asignada}")
            except Exception as e:
                print(f"{idx}/{total} ❌ Error de red: {url_asignada} -> {e}")

    print(f"\n✅ Descarga finalizada: {descargadas} imágenes guardadas.")

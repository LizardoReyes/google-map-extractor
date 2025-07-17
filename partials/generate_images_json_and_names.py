import json
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from partials.helpers import slugify

def generate_images_json_and_names(input_json: Path, output_json: Path, output_image_json: Path) -> None:
    # Leer archivo JSON de entrada
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    if "id" not in df.columns:
        raise ValueError("❌ La columna 'id' es requerida para generar nombres de imagen.")

    if "image" not in df.columns:
        df["image"] = ""

    images_data = []

    for _, row in df.iterrows():
        title = str(row["title"]).strip()
        slug_base = slugify(title)

        # Buscar primera URL válida
        image_url = ""
        for key in ["image_1", "image_2", "image_3"]:
            url = str(row.get(key, "")).strip()
            if url:
                image_url = url
                break

        if image_url:
            ext = Path(urlparse(image_url).path).suffix.lower()
            if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
                ext = ".jpg"
            image_name = f"{slug_base}{ext}"
            df.at[row.name, "image"] = image_name
        else:
            df.at[row.name, "image"] = ""

        images_data.append({
            "title": title,
            "city": row.get("city"),
            "categories": row.get("categories", ""),
            "image": df.at[row.name, "image"],
            "image_1": row.get("image_1", ""),
            "image_2": row.get("image_2", ""),
            "image_3": row.get("image_3", "")
        })

    # Guardar JSON principal actualizado
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

    # Guardar JSON de imágenes
    with open(output_image_json, 'w', encoding='utf-8') as f:
        json.dump(images_data, f, ensure_ascii=False, indent=2)

    print(f"✅ '{output_json.name}' y '{output_image_json.name}' generados exitosamente.")

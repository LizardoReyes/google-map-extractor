from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from partials.helpers import slugify  # Asegúrate de tener esta función


def generar_images_csv_y_nombres(input_csv: str, output_csv: str) -> None:
    input_path = Path(input_csv)
    df = pd.read_csv(input_path)

    if "id" not in df.columns:
        raise ValueError("❌ La columna 'id' es requerida para generar nombres de imagen.")

    if "image" not in df.columns:
        df["image"] = ""

    images_data = []

    for _, row in df.iterrows():
        title = str(row["title"]).strip()
        slug_base = slugify(title)
        row_id = int(row["id"])

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
            image_name = f"{slug_base}-{row_id}{ext}"
            df.at[row.name, "image"] = image_name
        else:
            df.at[row.name, "image"] = ""

        images_data.append({
            "title": title,
            "city": row.get("city"),
            "image": df.at[row.name, "image"],
            "image_1": row.get("image_1", ""),
            "image_2": row.get("image_2", ""),
            "image_3": row.get("image_3", "")
        })

    # Guardar resultados
    df.to_csv(input_path.with_name(output_csv), index=False)
    pd.DataFrame(images_data).to_csv(input_path.with_name("images.csv"), index=False)

    print(f"✅ Archivos generados:\n- {output_csv}\n- images.csv")

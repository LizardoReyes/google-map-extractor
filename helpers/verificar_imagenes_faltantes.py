import csv
import os
from pathlib import Path
import pandas as pd

def verificar_imagenes_faltantes(csv_path: str, carpeta_imagenes: str = "images", salida_csv: str = "imagenes_faltantes.csv") -> None:
    df = pd.read_csv(csv_path)
    imagenes_dir = Path(carpeta_imagenes)

    if "image" not in df.columns:
        print("❌ El archivo CSV no contiene la columna 'image'.")
        return

    faltantes = []

    for _, row in df.iterrows():
        nombre_imagen = str(row.get("image", "")).strip()
        if not nombre_imagen:
            faltantes.append(row)
            continue

        ruta_imagen = imagenes_dir / nombre_imagen
        if not ruta_imagen.exists():
            faltantes.append(row)

    if faltantes:
        df_faltantes = pd.DataFrame(faltantes)
        df_faltantes.to_csv(salida_csv, index=False)
        print(f"⚠️ Se encontraron {len(faltantes)} imágenes faltantes. Guardado en '{salida_csv}'")
    else:
        print("✅ Todas las imágenes están presentes en la carpeta.")

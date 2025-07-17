import pandas as pd
import json
import pyarrow
from pathlib import Path

def convert_json_to_csv(json_path: Path, csv_path: Path) -> None:
    """
    Convierte un archivo JSON a formato CSV usando el backend PyArrow para tipos eficientes.

    Args:
        json_path (Path): Ruta del archivo JSON de entrada.
        csv_path (Path): Ruta del archivo CSV de salida.
    """
    try:
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("❌ El JSON no contiene una lista de objetos.")

        # Crear el DataFrame y convertir tipos al backend pyarrow
        df = pd.DataFrame(data).convert_dtypes(dtype_backend="pyarrow")

        # Guardar como CSV
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"✅ Archivo CSV generado exitosamente en: {csv_path}")

    except Exception as e:
        print(f"❌ Error al convertir JSON a CSV: {e}")


def main():
    # Rutas de entrada y salida
    post_json_file = Path("../output/posts.json")
    post_csv_file = Path("../output/posts.csv")
    #categories_json_file = Path("output/categories.json")
    #categories_csv_file = Path("output/categories.csv")

    # Verificar existencia del archivo JSON
    if not post_json_file.exists():
        print(f"❌ El archivo de posts JSON no existe: {post_json_file}")
        return

    #if not categories_json_file.exists():
    #    print(f"❌ El archivo de categorías JSON no existe: {categories_json_file}")
    #    return

    # Convertir JSON a CSV
    convert_json_to_csv(post_json_file, post_csv_file)
    #convertir_json_a_csv(categories_json_file, categories_csv_file)


if __name__ == "__main__":
    main()

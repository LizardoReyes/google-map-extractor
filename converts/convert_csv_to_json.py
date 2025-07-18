from pathlib import Path

from partials.helper_csv import read_csv


def convert_csv_to_json(csv_path: Path, json_path: Path, orient: str = "records") -> None:
    """
    Convierte un archivo CSV a formato JSON usando el backend PyArrow para mayor eficiencia.

    Args:
        csv_path (Path): Ruta al archivo CSV de entrada.
        json_path (Path): Ruta al archivo JSON de salida.
        orient (str): Formato de salida de pandas (por defecto "records").
    """
    try:
        df = read_csv(csv_path, fallback_engine="python", dtype_backend="pyarrow")
        with json_path.open("w", encoding="utf-8") as f:
            f.write(df.to_json(orient=orient, force_ascii=False, indent=2))
        print(f"✅ Archivo JSON generado exitosamente en: {json_path}")
    except Exception as e:
        print(f"❌ Error al convertir CSV a JSON: {e}")


def main():
    # Definir rutas de entrada y salida
    post_csv_file = Path("../input/posts.csv")
    post_json_file = Path("../output/posts.json")
    #categories_csv_file = Path("../input/categories.csv")
    #categories_json_file = Path("../output/categories.json")

    # Verificar existencia del archivo CSV
    if not post_csv_file.exists():
        print(f"❌ El archivo CSV no existe: {post_csv_file}")
        return

    #if not categories_csv_file.exists():
    #    print(f"❌ El archivo de categorías CSV no existe: {categories_csv_file}")
    #    return

    # Convertir CSV a JSON
    convert_csv_to_json(post_csv_file, post_json_file, orient="records")
    #convert_csv_to_json(categories_csv_file, categories_json_file, orient="records")


if __name__ == "__main__":
    main()

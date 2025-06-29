from pathlib import Path
import pandas as pd

def convertir_csv_a_json(csv_path: Path, json_path: Path, orient: str = "records") -> None:
    """
    Convierte un archivo CSV a formato JSON.

    Args:
        csv_path (Path): Ruta al archivo CSV de entrada.
        json_path (Path): Ruta al archivo JSON de salida.
        orient (str): Formato de salida de pandas (por defecto "records").
    """
    try:
        df = pd.read_csv(csv_path)
        with json_path.open("w", encoding="utf-8") as f:
            f.write(df.to_json(orient=orient, force_ascii=False, indent=2))
        print(f"✅ Archivo JSON generado: {json_path.name}")
    except Exception as e:
        print(f"❌ Error con {csv_path.name}: {e}")

def main():
    carpeta = Path("businesses")
    if not carpeta.exists():
        print(f"❌ Carpeta no encontrada: {carpeta}")
        return

    # Buscar todos los .csv en la carpeta
    archivos_csv = list(carpeta.glob("*.csv"))

    if not archivos_csv:
        print(f"❌ No se encontraron archivos CSV en: {carpeta}")
        return

    for csv_file in archivos_csv:
        json_file = csv_file.with_suffix(".json")
        convertir_csv_a_json(csv_file, json_file, orient="records")

if __name__ == "__main__":
    main()

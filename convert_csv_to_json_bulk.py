from pathlib import Path

from convert_csv_to_json import convert_csv_to_json


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
        convert_csv_to_json(csv_file, json_file, orient="records")


if __name__ == "__main__":
    main()

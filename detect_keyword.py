from pathlib import Path

from partials.helper_csv import read_json_full
from partials.helpers import create_business


def detected_keywords(dir_business: Path):
    # Leemos 1 a cada archivo JSON en el directorio de negocios
    for file in dir_business.glob("*.json"):
        raw_data = read_json_full(ruta_archivo=file)
        business = create_business(raw_data)
        # Imprimimos el nombre del archivo  la clave keywords detectadas
        print(f"Archivo: {file.name}, Keywords detectadas: {business[0].query.split(' in ')[0]}")


def main():
    BASE_DIR = Path(__file__).resolve().parent
    DIR_BUSINESSES = BASE_DIR / "businesses"

    detected_keywords(dir_business=DIR_BUSINESSES)

if __name__ == "__main__":
    main()
"""
    Script para procesar un archivo CSV y convertirlo a JSON incluido los campos que son JSON.
    Este script lee un archivo CSV, intenta convertir cada campo que sea una cadena de texto con formato JSON válido en su estructura correspondiente (dict o list),
    y guarda el resultado en un archivo JSON.
"""

import csv
import json
import ast
from pathlib import Path

def clean_unicode_spaces(valor):
    if isinstance(valor, str):
        return valor.replace('\u202f', ' ')
    elif isinstance(valor, dict):
        return {k: clean_unicode_spaces(v) for k, v in valor.items()}
    elif isinstance(valor, list):
        return [clean_unicode_spaces(v) for v in valor]
    return valor

def try_parse_json(valor):
    if isinstance(valor, str):
        valor = valor.strip()
        if not valor:
            return valor
        # Intentar como JSON válido
        try:
            resultado = json.loads(valor)
            if isinstance(resultado, (dict, list)):
                return resultado
        except json.JSONDecodeError:
            pass
        # Intentar como literal de Python (con comillas simples)
        try:
            resultado = ast.literal_eval(valor)
            if isinstance(resultado, (dict, list)):
                return resultado
        except (ValueError, SyntaxError):
            pass
    return valor

def parse_row_fields(row):
    return {
        clave: clean_unicode_spaces(try_parse_json(valor))
        for clave, valor in row.items()
    }

def parse_csv_fields_to_json(input_csv, output_json):
    with input_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = [parse_row_fields(row) for row in reader]

    with output_json.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    input_file = Path("businesses/data.csv")
    output_file = Path("output/data.json")

    if not input_file.exists():
        print(f"El archivo {input_file} no existe.")
        return

    parse_csv_fields_to_json(input_file, output_file)
    print(f"Datos procesados y guardados en {output_file}")

if __name__ == "__main__":
    main()
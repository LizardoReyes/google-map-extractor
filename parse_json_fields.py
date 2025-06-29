import json

""" Por si fuiste inteligente y descargaste como CSV y no como JSON."""

"""Script para procesar campos JSON en un archivo JSON."""
""" Este script recorre un archivo JSON y convierte cualquier campo que sea una cadena de texto con formato JSON válido en su estructura correspondiente (dict o list).
"""

def intentar_parse_json(valor):
    if isinstance(valor, str):
        try:
            # Intenta decodificar como JSON
            resultado = json.loads(valor)
            # Solo lo reemplaza si el resultado es dict o list
            if isinstance(resultado, (dict, list)):
                return resultado
        except json.JSONDecodeError:
            pass
    return valor

def parsear_campos_json_recursivo(data):
    """
    Recorre un dict o lista de dicts y convierte cualquier string que sea JSON en su estructura correspondiente.
    """
    if isinstance(data, dict):
        return {
            clave: parsear_campos_json_recursivo(intentar_parse_json(valor))
            for clave, valor in data.items()
        }
    elif isinstance(data, list):
        return [
            parsear_campos_json_recursivo(intentar_parse_json(item))
            for item in data
        ]
    else:
        return data

def main():
    with open("output/businesses_raw.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data_procesada = parsear_campos_json_recursivo(data)
    with open("output/businesses_processed.json", "w", encoding="utf-8") as f:
        json.dump(data_procesada, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
import openai
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ruta de almacenamiento
PATH_IMAGES = Path("images")
PATH_IMAGES.mkdir(parents=True, exist_ok=True)

# Clave de API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image_dalle_for_business(name: str, city: str, categories: str, image_name: str, size="1024x1024") -> str:
    """
    Genera una imagen con DALL·E a partir de los datos del negocio.

    Args:
        name (str): Nombre del negocio.
        city (str): Ciudad donde se encuentra.
        categories (str): Categorías o tipo de negocio.
        image_name (str): Nombre del archivo de salida (ej. "imagen.jpg").
        size (str): Tamaño de imagen: "256x256", "512x512", o "1024x1024".

    Returns:
        str: Ruta local de la imagen generada o "" si falla.
    """
    image_path = PATH_IMAGES / image_name
    if image_path.exists():
        return str(image_path)

    prompt = f"Create a realistic image representing a business named '{name}' in the city of {city}, related to: {categories}. The scene should be visually appealing and descriptive."

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size,
            response_format="url"
        )

        image_url = response['data'][0]['url']
        img_data = requests.get(image_url, timeout=10).content
        with open(image_path, "wb") as f:
            f.write(img_data)

        return str(image_path)

    except Exception as e:
        print(f"[DALL·E] Error: {e}")
        return ""


def main():
    path = generate_image_dalle_for_business(
        name="Sagres Campo Pequeno",
        city="Lisboa",
        categories="sala de concertos, local para eventos",
        image_name="image.jpg"
    )
    print(f"✅ Imagen generada en: {path}")


if __name__ == "__main__":
    main()
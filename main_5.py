"""
    Script que utiliza OpenAI para generar contenido y crear imágenes.
"""

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# https://platform.openai.com/docs/models
def get_available_models() -> list:
    """
    Retrieves the list of available models from OpenAI.

    Returns:
        list: List of available model names.
    """
    models = client.models.list()
    return [model.id for model in models.data]

def get_dalle_models() -> list:
    """
    Retrieves the list of available DALL·E models from OpenAI.

    Returns:
        list: List of available DALL·E model names.
    """
    dalle_models = client.models.list()
    return [model.id for model in dalle_models.data if "dall-e" in model.id]

def get_gpt_models() -> list:
    """
    Retrieves the list of available GPT models from OpenAI.

    Returns:
        list: List of available GPT model names.
    """
    gpt_models = client.models.list()
    return [model.id for model in gpt_models.data if "gpt" in model.id]

def get_gpt_4_models() -> list:
    """
    Retrieves the list of available GPT-4 models from OpenAI.

    Returns:
        list: List of available GPT-4 model names.
    """
    gpt_4_models = client.models.list()
    return [model.id for model in gpt_4_models.data if "gpt-4" in model.id]


def create_content(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Generates content using OpenAI's GPT model.

    Args:
        prompt (str): The input prompt for content generation.
        model (str): The model to use for generation (default is "gpt-3.5-turbo").

    Returns:
        str: Generated content from the model.
    """
    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text


def generate_image(input: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=input,
        tools=[{"type": "image_generation"}],
    )

    # Save the image to a file
    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]

    if image_data:
        image_base64 = image_data[0]
        with open("otter.png", "wb") as f:
            f.write(base64.b64decode(image_base64))

def main():
    content = create_content("What is the capital of France?")
    print("Generated content:", content)
    #generate_image("Generate an image of gray tabby cat hugging an otter with an orange scarf")


if __name__ == "__main__":
    main()
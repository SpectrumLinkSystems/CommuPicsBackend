import os
from dotenv import load_dotenv, dotenv_values
import httpx


class ImageRecognitionService:
    async def recognize_image():
        load_dotenv()
        collections = [
            {"Animales": ["Mamíferos", "Aves", "Reptiles"]},
            {"Objetos": ["Juguetes", "Electrónica", "Ropa"]},
            {"Lugares": ["Parques", "Ciudades", "Montañas"]},
        ]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "¿Qué hay en esta imagen?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://cdn-icons-png.flaticon.com/512/648/648770.png",
                                "detail": "low",
                            },
                        },
                        {
                            "type": "text",
                            "text": """
                            Proporciona un nombre apropiado en español para buscar en la API de Arasaac y sugiere posibles colecciones y subcolecciones familiares a las que podría pertenecer, considerando que las categorías deberían ser fácilmente reconocibles para niños autistas de 5 a 12 años. 
                            No utilices términos genéricos como "Objeto". Si no encuentras una categoría adecuada, sugiere una nueva categoría que sea específica y familiar, como "Herramientas" para un destornillador, "Tecnología" para un ratón de computadora, etc.
                            La respuesta debe estar en formato JSON con la siguiente estructura:
                            {
                            "name": {PALABRA QUE REPRESENTA LA IMAGEN},
                            "optional_categories": [
                                {
                                "name": {NOMBRE DE LA POSIBLE CATEGORIA},
                                "optional_subcategories": [
                                    {
                                    "name": {NOMBRE DE LA SUBCATEGORIA}
                                    }
                                ]
                                }
                            ]
                            }
                            Lista de colecciones y subcolecciones existentes: {colecciones if colecciones else 'No hay colecciones disponibles, sugiere nuevas.'}
                            """,
                        },
                    ],
                }
            ],
            "max_tokens": 300,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            return response.json()

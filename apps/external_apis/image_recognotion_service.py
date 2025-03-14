from ast import List
import json
import os
from dotenv import load_dotenv, dotenv_values
import httpx


class ImageRecognitionService:
    async def recognize_image(self, image_url, collections:List):
        load_dotenv()
        #return json.dumps(collections)

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
                        {
                            "type": "text", 
                            "text": "A partir de este momento serás un especialista en autismo que ayudará a un niño a determinar qué objeto representa la siguiente imagen con el fin de que este niño pueda agregar un pictograma a su cuaderno PECS"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"{image_url}",
                                "detail": "low",
                            },
                        },
                        {
                            "type": "text",
                            "text": f"El niño cuenta con las siguientes colecciones: {json.dumps(collections, indent=4)}" + """ \n
                            Necesito que escojas la o las colecciones a las que el objeto reconocido pueda ingresar.
                            En el caso de que el objeto no encaje en ninguna de las colecciones existentes, recomendarás nuevas colecciones.
                            Quiero que la respuesta a esto SOLO sea un json que conserve la estructura de una colección existente.
                            Sin embargo quiero que tambien crees un campo extra para las nuevas colecciones que recomiendes como una coleccion de Strings.
                            En otras palabras necesito esto de respuesta: \n
                            {
                                recomendations: [
                                    {
                                        "id": "ID DE LA COLECCION",
                                        "name": "NOMBRE DE LA COLECCION",
                                        "image_url": "URL DE COLECCION",
                                        "child_id": "ID DEL NIÑO AL QUE LE PERTENECE LA COLECCION",
                                    },
                                ],
                                new_collections: ["CADA COLECCION NUEVA QUE RECOMIENDES"],
                                results: {
                                    "name": "NOMBRE DEL OBJETO RECONOCIDO"
                                }
                            }
                            """
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
            content_str = response.json()["choices"][0]["message"]["content"].strip("```json\n")
            
            try:
                json_content = json.loads(content_str)
                return json_content
            except json.JSONDecodeError as e:
                print("Error al decodificar el JSON:", e)

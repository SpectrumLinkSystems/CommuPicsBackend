from asgiref.sync import sync_to_async  # Importa sync_to_async
import json
import os
import random
from dotenv import load_dotenv
import httpx
from rest_framework.decorators import action
from rest_framework.response import Response
from adrf.viewsets import ViewSet
from apps.child.models.child import Child
from apps.child.models.collection import Collection
from apps.child.models.pictogram import Pictogram
from apps.child.serializers.pictogram_game_serializer import SentenceGamePictogramSerializer

load_dotenv()

class SentenceGameViewSet(ViewSet):
    
    async def generate_sentence_with_openai(self, pictograms, autism_level):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        }

        pictogram_names = [pic.name for pic in pictograms]
        
        if autism_level == 1:
            complexity_description = (
                "Oraciones muy simples con estructura 'sujeto + verbo + objeto'. "
                "No uses conjunciones. Usa solo los sujetos: 'yo', 'mamá' o 'papá'. "
                "Conjuga los verbos correctamente. Ejemplo: 'Yo como pan'."
            )
        elif autism_level == 2:
            complexity_description = (
                "Oraciones con cantidades y estructura simple. "
                "Usa solo los sujetos: 'yo', 'mamá' o 'papá'. "
                "Conjuga los verbos correctamente. Ejemplo: 'Yo quiero 2 galletas'."
            )
        elif autism_level == 3:
            complexity_description = (
                "Oraciones más elaboradas con adjetivos y conjunciones. "
                "Usa solo los sujetos: 'yo', 'mamá' o 'papá'. "
                "Conjuga los verbos correctamente. Ejemplo: 'Mamá come una manzana verde'."
            )
        else:
            complexity_description = "Oraciones simples."
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": f"""Eres un especialista en autismo que ayuda a niños a aprender a comunicarse.
                    A partir de estos pictogramas: {', '.join(pictogram_names)}, genera una oración corta con sentido para un niño con autismo de nivel {autism_level}.
                    La oración debe seguir la siguiente directriz de complejidad: {complexity_description}.
                    Usa solo los sujetos: "yo", "mamá" o "papá".
                    Conjuga los verbos correctamente según el sujeto.
                    Si hay verbos en infinitivo (como 'dormir', 'querer', 'lavar'), conjúgalos adecuadamente.
                    Devuelve la respuesta en formato JSON con dos campos:
                    - 'sentence': La oración generada.
                    - 'words': Un arreglo con las palabras de la oración ya conjugadas, en el orden correcto.
                    Ejemplo de respuesta:
                    {{
                        "sentence": "Yo quiero una galleta",
                        "words": ["Yo", "quiero", "una", "galleta"]
                    }}"""
                }
            ],
            "max_tokens": 100,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            print("Respuesta de OpenAI:", response.json())
            content_str = response.json()["choices"][0]["message"]["content"].strip()
            try:
                return json.loads(content_str)
            except json.JSONDecodeError:
                return {"sentence": content_str, "words": content_str.split()}

    @action(detail=False, methods=["post"], url_path="generate_sentence_game")
    async def generate_sentence_game(self, request):
        try:
            child_id = request.data.get("child_id")
            if not child_id:
                return Response({"error": "El campo 'child_id' es requerido."}, status=400)
            
            child = await sync_to_async(Child.objects.get)(id=child_id)
            
            autism_level = child.autism_level

            collections = await sync_to_async(list)(Collection.objects.filter(child_id=child))
            collection_ids = [collection.id for collection in collections]

            pictograms = await sync_to_async(list)(Pictogram.objects.filter(collection_id__in=collection_ids))
            
            if not pictograms:
                return Response({"error": "No hay pictogramas disponibles para este niño."}, status=404)

            collection_id = collections[0].id if collections else None
            
            openai_response = await self.generate_sentence_with_openai(pictograms, autism_level)
            generated_sentence = openai_response.get("sentence", "")
            words = openai_response.get("words", [])
            
            shuffled_words = words.copy()
            random.shuffle(shuffled_words)
            
            word_data = []
            for word in shuffled_words:
                word_data.append({
                    "name": word,
                    "image_url": "",
                    "arasaac_id": "9999",
                    "arasaac_categories": "",
                    "collection_id_id": collection_id
                })
            
            return Response({
                "shuffled_words": SentenceGamePictogramSerializer(word_data, many=True).data,
                "correct_order": words,
                "generated_sentence": generated_sentence
            }, status=200)
        
        except Child.DoesNotExist:
            return Response({"error": "El niño no existe."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
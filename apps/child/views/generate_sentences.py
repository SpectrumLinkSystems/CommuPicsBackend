from asgiref.sync import sync_to_async
import json
import os
import random
import spacy
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

nlp = spacy.load("es_core_news_sm")

class SentenceGameViewSet(ViewSet):
    
    async def generate_sentence_with_openai(self, pictograms, pronombres, autism_level):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer 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",
        }

        pictogram_names = [pic.name for pic in pictograms]
        pronombres_names = [pronombre.name for pronombre in pronombres]

        if autism_level == 3:
            complexity_description = (
                "Oraciones muy simples con estructura 'sujeto + verbo + objeto'. "
                "No uses conjunciones. Usa solo los siguientes sujetos: " + ", ".join(pronombres_names) + ". "
                "Conjuga los verbos correctamente. Ejemplo: 'Yo Como Pan'."
            )
        elif autism_level == 2:
            complexity_description = (
                "Oraciones con cantidades y estructura simple. "
                "Usa solo los siguientes sujetos: " + ", ".join(pronombres_names) + ". "
                "Conjuga los verbos correctamente. Ejemplo: 'Yo Quiero Dos Galletas'."
            )
        elif autism_level == 1:
            complexity_description = (
                "Oraciones más elaboradas con adjetivos relacionados al objeto. "
                "Usa solo los siguientes sujetos: " + ", ".join(pronombres_names) + ". "
                "Conjuga los verbos correctamente. Ejemplo: 'Mamá Come Uno Galleta Caliente'."
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
                    Usa solo los siguientes sujetos: {', '.join(pronombres_names)}.
                    **Usa solo las siguientes palabras: {', '.join(pictogram_names)}.**
                    **Los verbos deben estar en infinitivo (por ejemplo, "Comer" en lugar de "Come").**
                    **Asegúrate de que la primera letra de cada palabra en la oración sea mayúscula.**
                    **Los números deben estar en su forma masculina (por ejemplo, "Uno" en lugar de "Una").**
                    Devuelve **solo un objeto JSON** con dos campos:
                    - 'sentence': La oración generada.
                    - 'words': Un arreglo con las palabras de la oración ya conjugadas, en el orden correcto.
                    Ejemplo de respuesta:
                    {{
                        "sentence": "Yo Querer Uno Galleta",
                        "words": ["Yo", "Querer", "Uno", "Galleta"]
                    }}"""
                }
            ],
            "max_tokens": 200,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )
            #print("Respuesta de OpenAI:", response.json())
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
            if not collections:
                return Response({"error": "El niño no tiene colecciones."}, status=404)

            first_collection = collections[0]
            collection_id = first_collection.id

            pictograms = await sync_to_async(list)(Pictogram.objects.filter(collection_id__in=[col.id for col in collections]))
            
            if not pictograms:
                return Response({"error": "No hay pictogramas disponibles para este niño."}, status=404)

            pictogram_dict = {pic.name: pic for pic in pictograms}

            pronombres_collection = next(
                (collection for collection in collections if collection.name == "Pronombres"), None
            )
            if not pronombres_collection:
                return Response({"error": "No se encontró la colección de pronombres para este niño."}, status=404)

            pronombres = await sync_to_async(list)(Pictogram.objects.filter(collection_id=pronombres_collection.id))
            
            openai_response = await self.generate_sentence_with_openai(pictograms, pronombres, autism_level)
            generated_sentence = openai_response.get("sentence", "")
            words = openai_response.get("words", [])
            
            shuffled_words = words.copy()
            random.shuffle(shuffled_words)
            
            word_data = []
            for word in shuffled_words:

                pictogram = pictogram_dict.get(word)
                if pictogram:
                    word_data.append({
                        "name": pictogram.name,
                        "image_url": pictogram.image_url,
                        "arasaac_id": pictogram.arasaac_id,
                        "arasaac_categories": pictogram.arasaac_categories,
                        "collection_id": pictogram.collection_id_id
                    })
                else:
                    word_data.append({
                        "name": word,
                        "image_url": "",
                        "arasaac_id": "9999",
                        "arasaac_categories": "",
                        "collection_id": collection_id
                    })
                    
            serialized_data = SentenceGamePictogramSerializer(word_data, many=True).data
            
            return Response({
                "shuffled_words": serialized_data,
                "correct_order": words,
                "generated_sentence": generated_sentence
            }, status=200)
        
        except Child.DoesNotExist:
            return Response({"error": "El niño no existe."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
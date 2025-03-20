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
from apps.child.services.default_collections import DEFAULT_COLLECTIONS

load_dotenv()

class SentenceGameViewSet(ViewSet):
    
    async def generate_sentence_with_openai(self, pictograms, autism_level):
        """
        Genera una oración con sentido y conjuga los verbos usando OpenAI.
        Toma en cuenta el nivel de autismo para adaptar la complejidad de la oración.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        }

        # Crear una lista de nombres de pictogramas
        pictogram_names = [pic.name for pic in pictograms]

        # Definir la complejidad de la oración según el nivel de autismo
        complexity_description = {
            1: "oraciones muy simples, con sujeto + verbo + objeto, y palabras básicas.",
            2: "oraciones un poco más complejas, con conectores como 'y' o 'en', y vocabulario un poco más amplio.",
            3: "oraciones complejas, con adjetivos, conectores y estructura gramatical completa."
        }.get(autism_level, "oraciones simples.")

        payload = {
            "model": "gpt-4o-mini",  # Puedes usar "gpt-3.5-turbo" si prefieres
            "messages": [
                {
                    "role": "user",
                    "content": f"""Eres un especialista en autismo que ayuda a niños a aprender a comunicarse.
                    A partir de estos pictogramas: {', '.join(pictogram_names)}, genera una oración con sentido que un niño con autismo de nivel {autism_level} pueda entender.
                    La oración debe ser {complexity_description}
                    Además, conjuga los verbos correctamente según el sujeto.
                    Devuelve la respuesta en formato JSON con dos campos:
                    - 'sentence': La oración generada.
                    - 'words': Un arreglo con las palabras de la oración ya conjugadas, en el orden correcto.
                    Ejemplo de respuesta:
                    {{
                        "sentence": "Él corre en el parque",
                        "words": ["Él", "corre", "en", "el", "parque"]
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
            content_str = response.json()["choices"][0]["message"]["content"].strip()
            try:
                return json.loads(content_str)  # Parsear la respuesta JSON
            except json.JSONDecodeError:
                return {"sentence": content_str, "words": content_str.split()}  # Fallback si no es JSON válido
    
    @action(detail=False, methods=["post"], url_path="generate_sentence_game")
    async def generate_sentence_game(self, request):
        try:
            child_id = request.data.get("child_id")
            if not child_id:
                return Response({"error": "El campo 'child_id' es requerido."}, status=400)
            
            # Usar sync_to_async para acceder al ORM de Django
            child = await sync_to_async(Child.objects.get)(id=child_id)
            
            # Obtener la complejidad de la oración basada en el nivel de autismo
            autism_level = child.autism_level
            sentence_complexity = self.get_sentence_complexity(autism_level)
            
            # Obtener todas las colecciones del niño
            collections = await sync_to_async(Collection.objects.filter)(child_id=child)
            collection_ids = await sync_to_async(list)(collections.values_list('id', flat=True))  # Extraer los IDs de las colecciones

            # Obtener todos los pictogramas de todas las colecciones del niño
            pictograms = await sync_to_async(Pictogram.objects.filter)(collection_id__in=collection_ids)
            
            if not await sync_to_async(pictograms.exists)():
                return Response({"error": "No hay pictogramas disponibles para este niño."}, status=404)

            # Obtener pronombres y conjunciones de las colecciones por defecto
            pronouns = self.get_pictograms_by_category("Pronombres")
            conjunctions = self.get_pictograms_by_category("Conjunciones")

            # Obtener el ID de la primera colección del niño
            collection_id = await sync_to_async(lambda: collections.first().id)()

            # Generar una oración desordenada
            sentence_pictograms = await sync_to_async(self.select_pictograms_for_sentence)(
                sentence_complexity,  # Complejidad de la oración
                pictograms,           # Pictogramas disponibles
                pronouns,             # Pronombres
                conjunctions,         # Conjunciones
                collection_id         # Pasar el collection_id
            )
            if not sentence_pictograms:
                return Response({"error": "No hay suficientes pictogramas para generar una oración."}, status=404)
            
            # Generar una oración con sentido y palabras conjugadas usando OpenAI
            openai_response = await self.generate_sentence_with_openai(sentence_pictograms, autism_level)
            generated_sentence = openai_response.get("sentence", "")
            words = openai_response.get("words", [])
            
            # Guardar el orden correcto de las palabras
            correct_order = words  # Usar las palabras ya conjugadas y ordenadas
            
            # Mezclar las palabras para el juego
            shuffled_words = words.copy()
            random.shuffle(shuffled_words)
            
            # Convertir cada palabra a un formato adecuado para la serialización
            word_data = []
            for word in shuffled_words:
                word_data.append({
                    "name": word,
                    "image_url": "",  # Puedes agregar una URL de imagen si es necesario
                    "arasaac_id": "9999",  # ID genérico
                    "arasaac_categories": "",  # Categoría genérica
                    "collection_id_id": collection_id
                })
            
            return Response({
                "shuffled_words": SentenceGamePictogramSerializer(word_data, many=True).data,
                "correct_order": correct_order,
                "generated_sentence": generated_sentence  # Incluir la oración generada
            }, status=200)
        
        except Child.DoesNotExist:
            return Response({"error": "El niño no existe."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    def get_sentence_complexity(self, autism_level):
        if autism_level == 1:
            return "simple"
        elif autism_level == 2:
            return "medium"
        elif autism_level == 3:
            return "complex"
        else:
            return "simple"  # Valor por defecto
    
    def get_pictograms_by_category(self, category_name):
        # Obtener pictogramas de una colección por defecto basada en el nombre de la categoría
        for collection in DEFAULT_COLLECTIONS:
            if collection["name"] == category_name:
                return collection["pictograms"]
        return []
    
    def select_pictograms_for_sentence(self, complexity, pictograms, pronouns, conjunctions, collection_id):
        # Crear instancias de pictogramas como diccionarios
        def create_temp_pictogram(name, category):
            return {
                'name': name,
                'image_url': "",
                'arasaac_id': "9999",
                'arasaac_categories': category,
                'collection_id_id': collection_id
            }
        
        # Convertir pronouns y conjunctions a instancias de Pictogram si son diccionarios
        def ensure_pictogram(pic):
            if isinstance(pic, dict):
                return Pictogram(**pic)  # Crear una instancia temporal de Pictogram
            return pic
        
        pronouns = [ensure_pictogram(p) for p in pronouns]
        conjunctions = [ensure_pictogram(c) for c in conjunctions]
        
        if complexity == "simple":
            # Oraciones simples: Sujeto + Verbo + Objeto
            subject = random.choice(pronouns) if pronouns else create_temp_pictogram("Yo", "pronoun")
            verb = pictograms.filter(arasaac_categories__icontains="verb").first()
            obj = pictograms.filter(arasaac_categories__icontains="object").exclude(arasaac_categories__icontains="color").first()
            
            if not verb:
                verb = pictograms.first()
            if not obj:
                obj = pictograms.exclude(id=verb.id).first() if verb else pictograms.first()
            
            if not verb or not obj:
                return []
            
            return [subject, verb, obj]
        
        elif complexity == "medium":
            # Oraciones con conectores: Sujeto + Verbo + Objeto + Conjunción + Objeto
            subject = random.choice(pronouns) if pronouns else create_temp_pictogram("Yo", "pronoun")
            verb = pictograms.filter(arasaac_categories__icontains="verb").first()
            obj1 = pictograms.filter(arasaac_categories__icontains="object").exclude(arasaac_categories__icontains="color").first()
            conjunction = random.choice(conjunctions) if conjunctions else create_temp_pictogram("y", "conjunction")
            obj2 = pictograms.filter(arasaac_categories__icontains="object").exclude(arasaac_categories__icontains="color").exclude(id=obj1.id).first() if obj1 else None
            
            if not verb or not obj1 or not obj2:
                return []
            
            return [subject, verb, obj1, conjunction, obj2]
        
        elif complexity == "complex":
            # Oraciones complejas: Sujeto + Verbo + Objeto + Conjunción + Adjetivo + Objeto
            subject = random.choice(pronouns) if pronouns else create_temp_pictogram("Yo", "pronoun")
            verb = pictograms.filter(arasaac_categories__icontains="verb").first()
            obj1 = pictograms.filter(arasaac_categories__icontains="object").exclude(arasaac_categories__icontains="color").first()
            conjunction = random.choice(conjunctions) if conjunctions else create_temp_pictogram("y", "conjunction")
            adjective = pictograms.filter(arasaac_categories__icontains="adjective").first()
            obj2 = pictograms.filter(arasaac_categories__icontains="object").exclude(arasaac_categories__icontains="color").exclude(id=obj1.id).first() if obj1 else None
            
            if not verb or not obj1 or not obj2 or not adjective:
                return []
            
            return [subject, verb, obj1, conjunction, adjective, obj2]
        
        else:
            return []
    
    def shuffle_pictograms(self, pictograms):
        shuffled = list(pictograms)
        random.shuffle(shuffled)
        return shuffled
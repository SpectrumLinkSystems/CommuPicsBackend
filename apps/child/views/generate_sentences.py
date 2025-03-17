from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.db.models import Q
from apps.child.models.child import Child
from apps.child.models.collection import Collection
from apps.child.models.pictogram import Pictogram
import random

from apps.child.serializers.pictogram_game_serializer import SentenceGamePictogramSerializer
from apps.child.services.default_collections import DEFAULT_COLLECTIONS

class SentenceGameViewSet(ViewSet):
    
    # Agregar OpenAI para mejorar la generación de oraciones (reemplazar con un servicio de IA)
    # OPENAI_API_KEY = "your-openai-api-key" 
    # Diccionario de conjugaciones de verbos (reemplazar con un servicio de conjugación de verbos)
    VERB_CONJUGATIONS = {
        "yo": {
            "correr": "corro",
            "comer": "como",
            "saltar": "salto",
            "Empujar": "empuja"
        },
        "él": {
            "correr": "corre",
            "comer": "come",
            "saltar": "salta",
            "Empujar": "empuja"
        },
    }
    
    @action(detail=False, methods=["post"], url_path="generate_sentence_game")
    def generate_sentence_game(self, request):
        try:
            child_id = request.data.get("child_id")
            if not child_id:
                return Response({"error": "El campo 'child_id' es requerido."}, status=400)
            
            child = Child.objects.get(id=child_id)
            
            sentence_complexity = self.get_sentence_complexity(child.autism_level)
            
            collections = Collection.objects.filter(child_id=child)
            collection_ids = collections.values_list('id', flat=True)

            pictograms = Pictogram.objects.filter(collection_id__in=collection_ids)
            print("Pictogramas en las colecciones del niño:", pictograms.values_list("name", flat=True))
            
            if not pictograms.exists():
                return Response({"error": "No hay pictogramas disponibles para este niño."}, status=404)

            pronouns = self.get_pictograms_by_category("Pronombres")
            conjunctions = self.get_pictograms_by_category("Conjunciones")

            # Obtener el ID de la primera colección del niño
            collection_id = collections.first().id

            # Generar una oración desordenada
            sentence_pictograms = self.select_pictograms_for_sentence(
                sentence_complexity,  # Complejidad de la oración
                pictograms,           # Pictogramas disponibles
                pronouns,             # Pronombres
                conjunctions,         # Conjunciones
                collection_id         # Pasar el collection_id
            )
            if not sentence_pictograms:
                return Response({"error": "No hay suficientes pictogramas para generar una oración."}, status=404)
            
            # Guardar el orden correcto antes de mezclar
            correct_order = []
            for pic in sentence_pictograms:
                if isinstance(pic, Pictogram) and hasattr(pic, 'id') and pic.id:
                    correct_order.append(pic.id)
                elif isinstance(pic, dict) and 'id' in pic:
                    correct_order.append(pic['id'])
                elif isinstance(pic, dict) and 'name' in pic:
                    correct_order.append(pic['name'])
                elif hasattr(pic, 'name'):
                    correct_order.append(pic.name)
                else:
                    # Un identificador genérico si no hay otra opción
                    correct_order.append(str(random.randint(10000, 99999)))
            
            # Mezclar los pictogramas
            shuffled_pictograms = self.shuffle_pictograms(sentence_pictograms)
            
            # Convertir cada pictograma a un formato adecuado para la serialización
            pictogram_data = []
            for pic in shuffled_pictograms:
                if isinstance(pic, Pictogram) and pic.id:
                    # Si es un objeto Pictogram con ID, simplemente usar el objeto
                    pictogram_data.append(pic)
                elif isinstance(pic, dict):
                    # Si ya es un diccionario, asegurarse de que tenga collection_id_id
                    if 'collection_id_id' not in pic and 'collection_id' in pic:
                        pic['collection_id_id'] = pic['collection_id']
                    pictogram_data.append(pic)
                else:
                    # Si es un pictograma temporal, crear un diccionario con los datos
                    try:
                        data = {
                            'name': pic.name if hasattr(pic, 'name') else "Pictograma",
                            'image_url': pic.image_url if hasattr(pic, 'image_url') else "",
                            'arasaac_id': pic.arasaac_id if hasattr(pic, 'arasaac_id') else "9999",
                            'arasaac_categories': pic.arasaac_categories if hasattr(pic, 'arasaac_categories') else "",
                            'collection_id_id': collection_id
                        }
                        pictogram_data.append(data)
                    except Exception as e:
                        print(f"Error procesando pictograma: {e}")
                        print(f"Tipo de pictograma: {type(pic)}")
                        # Si hay error, crear un pictograma genérico
                        pictogram_data.append({
                            'name': "Pictograma genérico",
                            'image_url': "",
                            'arasaac_id': "9999",
                            'arasaac_categories': "",
                            'collection_id_id': collection_id
                        })
            
            return Response({
                "shuffled_pictograms": SentenceGamePictogramSerializer(pictogram_data, many=True).data,
                "correct_order": correct_order
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
            return "simple"
    
    def get_pictograms_by_category(self, category_name):
        for collection in DEFAULT_COLLECTIONS:
            if collection["name"] == category_name:
                return collection["pictograms"]
        return []
    
    def select_pictograms_for_sentence(self, complexity, pictograms, pronouns, conjunctions, collection_id):
        #print("Pictogramas disponibles:", pictograms.values_list("name", flat=True))

        def create_temp_pictogram(name, category):
            return {
                'name': name,
                'image_url': "",
                'arasaac_id': "9999",
                'arasaac_categories': category,
                'collection_id_id': collection_id
            }
        
        def ensure_pictogram(pic):
            if isinstance(pic, dict):
                return Pictogram(**pic)
            return pic
        
        pronouns = [ensure_pictogram(p) for p in pronouns]
        conjunctions = [ensure_pictogram(c) for c in conjunctions]
        
        if complexity == "simple":
            # Oraciones simples: Sujeto + Verbo + Objeto
            subject = random.choice(pronouns) if pronouns else create_temp_pictogram("Yo", "pronoun")
            verb_list = list(pictograms.filter(arasaac_categories__icontains="verb"))
            verb = random.choice(verb_list) if verb_list else None
            obj_list = list(pictograms.filter(arasaac_categories__icontains="object"
                                            ).exclude(arasaac_categories__icontains="color"
                                            ).exclude(arasaac_categories__icontains="shape"))

            obj = random.choice(obj_list) if obj_list else None
            #print("Verbos encontrados:", verb)
            #print("Objetos encontrados:", obj)
            
            # Si no hay verbos u objetos, usar cualquier pictograma
            if not verb:
                verb = pictograms.first()
            if not obj:
                obj = pictograms.exclude(id=verb.id).first() if verb else pictograms.first()
            
            if not verb or not obj:
                return []
            
            if subject.name in self.VERB_CONJUGATIONS and verb.name in self.VERB_CONJUGATIONS[subject.name]:
                verb.name = self.VERB_CONJUGATIONS[subject.name][verb.name]
            
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
            
            if subject.name in self.VERB_CONJUGATIONS and verb.name in self.VERB_CONJUGATIONS[subject.name]:
                verb.name = self.VERB_CONJUGATIONS[subject.name][verb.name]
            
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
            
            if subject.name in self.VERB_CONJUGATIONS and verb.name in self.VERB_CONJUGATIONS[subject.name]:
                verb.name = self.VERB_CONJUGATIONS[subject.name][verb.name]
            
            return [subject, verb, obj1, conjunction, adjective, obj2]
        
        else:
            return []
    
    def shuffle_pictograms(self, pictograms):
        shuffled = list(pictograms)
        random.shuffle(shuffled)
        return shuffled
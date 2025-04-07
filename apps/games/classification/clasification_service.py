# apps/game/services/game_service.py
import random
from django.db import transaction
from django.db.models import Count
from apps.child.models import Collection, Pictogram

class ClassificationService:
    @staticmethod
    def select_random_collections(child_id):

        collections = Collection.objects.filter(child_id=child_id)
        
        if collections.count() < 2:
            return None
            
        collections_list = list(collections)
        random.shuffle(collections_list)
        return collections_list[:2]

    @staticmethod
    def get_pictograms_for_game(child_id, collection_ids):

        try:

            collection_ids = [int(cid) for cid in collection_ids]
            if len(collection_ids) != 2:
                raise ValueError("Se requieren exactamente 2 IDs de colección")
            
            valid_collections = Collection.objects.filter(
                id__in=collection_ids, 
                child_id=child_id
            ).values_list('id', flat=True)
            
            if len(valid_collections) != 2:
                raise ValueError("Una o más colecciones no pertenecen al niño o no existen")

            pictograms = []
            for col_id in collection_ids:

                col_pictograms = list(
                    Pictogram.objects.filter(
                        collection_id=col_id
                    ).annotate(
                        usage_count=Count('pictogramusage')
                    ).order_by('usage_count', '?')[:3]
                    .values('id', 'name', 'image_url', 'arasaac_id', 'arasaac_categories', 'collection_id')
                )
                pictograms.extend(col_pictograms)
            
            random.shuffle(pictograms)
            return pictograms[:6]
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Datos inválidos: {str(e)}")
        
    @staticmethod
    @transaction.atomic
    def check_classification(child_id, pictogram_id, collection_id):
        try:

            child_id = int(child_id)
            pictogram_id = int(pictogram_id)
            
            if isinstance(collection_id, Collection):
                collection_id = collection_id.id
            collection_id = int(collection_id)

            if not Collection.objects.filter(id=collection_id, child_id_id=child_id).exists():
                raise ValueError("La colección no pertenece al niño")

            pictogram = Pictogram.objects.filter(id=pictogram_id).values('collection_id').first()
            if not pictogram:
                raise ValueError("Pictograma no encontrado")
            
            correct_collection_id = pictogram['collection_id']

            correct_collection_name = Collection.objects.filter(
                id=correct_collection_id
            ).values_list('name', flat=True).first() or ""

            return {
                'is_correct': correct_collection_id == collection_id,
                'correct_collection_id': correct_collection_id,
                'correct_collection_name': correct_collection_name,
                'pictogram_id': pictogram_id,
                'selected_collection_id': collection_id
            }
            
        except Exception as e:
            raise ValueError(f"Error en la clasificación: {str(e)}")
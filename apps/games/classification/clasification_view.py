# apps/game/views.py
from adrf import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from apps.child.models.collection import Collection
from apps.child.models.pictogram import Pictogram
from apps.games.classification.clasification_service import ClassificationService
from apps.games.game_serializer import ClassificationCheckSerializer, ClassificationResultSerializer, CollectionSerializer, PictogramSerializer

class ClassificationGameViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'], url_path='collections/(?P<child_id>[^/.]+)')
    def get_game_collections(self, request, child_id=None):
        """
        Obtiene 2 colecciones aleatorias para iniciar el juego
        """
        try:
            collections = ClassificationService.select_random_collections(child_id)
            
            if not collections:
                return Response(
                    {"detail": "El niño necesita al menos 2 colecciones para jugar"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Usar el serializador para convertir a JSON
            serializer = CollectionSerializer(collections, many=True)
            return Response({
                'collections': serializer.data,
                'child_id': child_id
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='pictograms/(?P<child_id>[^/.]+)')
    def get_game_pictograms(self, request, child_id=None):
        try:
            collection_ids = request.query_params.getlist('collection_ids', [])
            
            if not collection_ids:
                return Response(
                    {"detail": "Se requieren IDs de colección"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            pictograms = ClassificationService.get_pictograms_for_game(child_id, collection_ids)
            
            correct_answers = {
                str(pic['id']): pic['collection_id'] 
                for pic in pictograms
            }
            
            return Response({
                'pictograms': pictograms,
                'correct_answers': correct_answers,
                'collection_ids': collection_ids
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": f"Error interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['post'], url_path='check-classification/(?P<child_id>[^/.]+)')
    def check_classification(self, request, child_id=None):
        try:
            pictogram_id = request.data.get('pictogram_id')
            collection_id = request.data.get('collection_id')
            
            if not all([pictogram_id, collection_id]):
                return Response(
                    {"detail": "Se requieren pictogram_id y collection_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            result = ClassificationService.check_classification(
                child_id=child_id,
                pictogram_id=pictogram_id,
                collection_id=collection_id
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Pictogram.DoesNotExist:
            return Response(
                {"detail": "El pictograma no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Collection.DoesNotExist:
            return Response(
                {"detail": "La colección no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Error interno: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
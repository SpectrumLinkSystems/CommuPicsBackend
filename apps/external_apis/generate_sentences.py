from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.db.models import Q
from .models import Child, Pictogram, Collection
from .serializers import PictogramSerializer

class SentenceGeneratorViewSet(ViewSet):
    
    @action(detail=False, methods=["post"], url_path="generate_sentence")
    def generate_sentence(self, request):

        try:
            child_id = request.data.get("child_id")
            child = Child.objects.get(id=child_id)
            
            collection = Collection.objects.filter(child_id=child).first()
            if not collection:
                return Response({"error": "El niño no tiene una colección asignada."}, status=404)
            
            pictograms = Pictogram.objects.filter(collection_id=collection)
            
            
            if not pictograms.exists():
                return Response({"error": "No hay pictogramas disponibles para este niño."}, status=404)

            if child.sentence_complexity == "simple":

                pictograms = pictograms.exclude(arasaac_categories__icontains="conjunction")
                sentence = f"Quiero {pictograms.first().name}" if pictograms.exists() else "No se encontraron pictogramas adecuados."
            
            elif child.sentence_complexity == "complex":

                verbs = pictograms.filter(arasaac_categories__icontains="verb")
                objects = pictograms.filter(arasaac_categories__icontains="object")
                conjunctions = pictograms.filter(arasaac_categories__icontains="conjunction")
                
                subject = "Yo"
                verb = verbs.first().name if verbs.exists() else "quiero"
                obj = objects.first().name if objects.exists() else "algo"
                connector = conjunctions.first().name if conjunctions.exists() else ""
                
                sentence = f"{subject} {verb} {obj} {connector}".strip()
            
            else:
                sentence = "Configuración de complejidad no válida."
            
            return Response({"sentence": sentence}, status=200)
        
        except Child.DoesNotExist:
            return Response({"error": "El niño no existe."}, status=404)
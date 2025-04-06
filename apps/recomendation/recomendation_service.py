import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Sum
from apps.child.models.collection import Collection
from apps.child.models.pictogram import Pictogram, PictogramUsage
from datetime import datetime

def get_pictogram_recommendations(child_id, selected_pictogram_id):
    def count_shared_categories(categories1, categories2):
        set1 = set(cat.strip().lower() for cat in categories1.split(",") if cat.strip())
        set2 = set(cat.strip().lower() for cat in categories2.split(",") if cat.strip())
        return len(set1 & set2)

    selected_pictogram = Pictogram.objects.get(id=selected_pictogram_id)
    
    # Obtener las colecciones asociadas al niño específico
    collections = Collection.objects.filter(child_id=child_id)
    
    # Obtener los IDs de las colecciones asociadas al niño
    collection_ids = collections.values_list('id', flat=True)
    
    pictogram_usage = PictogramUsage.objects.filter(child_id=child_id).select_related('pictogram')
    
    used_pictograms = []
    for usage in pictogram_usage:
        pictogram = usage.pictogram
        used_pictograms.append({
            'name': pictogram.name,
            'arasaac_categories': pictogram.arasaac_categories,
            'cant_used': usage.cant_used,
            'pictogram': pictogram
        })
    
    all_pictograms = Pictogram.objects.filter(collection_id__in=collection_ids)
    
    default_pictograms = [
        {
            'name': pic.name,
            'arasaac_categories': pic.arasaac_categories,
            'cant_used': 0,
            'pictogram': pic
        }
        for pic in all_pictograms if pic.id not in [u['pictogram'].id for u in used_pictograms]
    ]
    
    all_pictograms = used_pictograms + default_pictograms
    
    # Filtrar pictogramas que comparten al menos 2 categorías
    relevant_pictograms = [
        pic for pic in all_pictograms
        if pic['pictogram'].id != selected_pictogram_id and
        count_shared_categories(selected_pictogram.arasaac_categories, pic['arasaac_categories']) >= 2
    ]
    
    if not relevant_pictograms:
        return {"error": "No hay pictogramas relevantes para recomendar (que compartan al menos 2 categorías)."}
    
    # Preprocesamiento de texto para TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([pic['arasaac_categories'] for pic in relevant_pictograms])
    
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Encontrar el índice del pictograma seleccionado (para calcular similitudes)
    selected_categories = selected_pictogram.arasaac_categories
    selected_idx = None
    max_shared = -1
    
    for i, pic in enumerate(relevant_pictograms):
        shared = count_shared_categories(selected_categories, pic['arasaac_categories'])
        if shared > max_shared:
            max_shared = shared
            selected_idx = i
    
    sim_scores = list(enumerate(similarity_matrix[selected_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Aplicar ponderación por uso
    weighted_scores = []
    for idx, score in sim_scores:
        pictogram = relevant_pictograms[idx]
        shared_cats = count_shared_categories(selected_categories, pictogram['arasaac_categories'])
        weighted_score = score * (1 + (pictogram['cant_used'] / 100)) * (1 + shared_cats * 0.2)
        weighted_scores.append((idx, weighted_score))
    
    weighted_scores = sorted(weighted_scores, key=lambda x: x[1], reverse=True)
    
    # Seleccionar los mejores pictogramas
    top_pictograms = []
    seen_ids = set()
    for idx, _ in weighted_scores:
        pictogram = relevant_pictograms[idx]
        if pictogram['pictogram'].id not in seen_ids:
            seen_ids.add(pictogram['pictogram'].id)
            top_pictograms.append(pictogram)
        if len(top_pictograms) >= 6:
            break
    
    # Formatear las recomendaciones
    recommendations = [
        {
            "child": child_id,
            "pictogram": pic['pictogram'].id,
            "pictogram_data": {
                "id": pic['pictogram'].id,
                "name": pic['pictogram'].name,
                "image_url": pic['pictogram'].image_url,
                "arasaac_id": pic['pictogram'].arasaac_id,
                "arasaac_categories": pic['pictogram'].arasaac_categories,
            },
            "date_used": datetime.now().isoformat(),
            "cant_used": pic['cant_used'],
            "shared_categories": count_shared_categories(selected_categories, pic['arasaac_categories'])
        }
        for pic in top_pictograms
    ]
    
    return {"recomendaciones": recommendations}
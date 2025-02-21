import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Sum
from apps.child.models.pictogram import Pictogram, PictogramUsage
from datetime import datetime

def get_pictogram_recommendations(child_id, selected_pictogram_id):

    selected_pictogram = Pictogram.objects.get(id=selected_pictogram_id)
    
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
    
    all_pictograms = Pictogram.objects.all()
    
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
    
    selected_categories = set(selected_pictogram.arasaac_categories.split(", "))
    
    relevant_pictograms = [
        pic for pic in all_pictograms
        if selected_categories.intersection(set(pic['arasaac_categories'].split(", ")))
        and pic['pictogram'].id != selected_pictogram_id
    ]
    
    if not relevant_pictograms:
        return {"error": "No hay pictogramas relevantes para recomendar."}
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([pic['arasaac_categories'] for pic in relevant_pictograms])
    
    similarity_matrix = cosine_similarity(tfidf_matrix)

    selected_idx = next((i for i, pic in enumerate(relevant_pictograms) if pic['pictogram'].id == selected_pictogram_id), None)

    selected_idx = selected_idx if selected_idx is not None else 0

    sim_scores = list(enumerate(similarity_matrix[selected_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    

    weighted_scores = []
    for idx, score in sim_scores:
        pictogram = relevant_pictograms[idx]
        weighted_score = score * (1 + pictogram['cant_used'] / 100) 
        weighted_scores.append((idx, weighted_score))
    
    weighted_scores = sorted(weighted_scores, key=lambda x: x[1], reverse=True)
    
    top_pictograms = []
    for idx, _ in weighted_scores:
        pictogram = relevant_pictograms[idx]
        if pictogram['pictogram'].id != selected_pictogram_id and pictogram not in top_pictograms:
            top_pictograms.append(pictogram)
        if len(top_pictograms) >= 6:
            break
    
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
            "cant_used": pic['cant_used']
        }
        for pic in top_pictograms
    ]
    
    return {"recomendaciones": recommendations}
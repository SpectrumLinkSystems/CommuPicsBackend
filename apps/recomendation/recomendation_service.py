import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Sum
from apps.child.models.pictogram import Pictogram, PictogramUsage
from datetime import datetime

def get_pictogram_recommendations(child_id, selected_pictogram_id):

    selected_pictogram = Pictogram.objects.get(id=selected_pictogram_id)
    
    pictograms = Pictogram.objects.all()
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
    
    if not used_pictograms:
        return {"error": "El niño no ha utilizado pictogramas previamente."}

    selected_categories = set(selected_pictogram.arasaac_categories.split(", "))

    relevant_pictograms = [
        pic for pic in used_pictograms
        if selected_categories.intersection(set(pic['arasaac_categories'].split(", ")))
    ]

    if not relevant_pictograms:
        return {"error": "No hay pictogramas relevantes para recomendar."}

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([pic['arasaac_categories'] for pic in relevant_pictograms])

    similarity_matrix = cosine_similarity(tfidf_matrix)

    selected_idx = next((i for i, pic in enumerate(relevant_pictograms) if pic['pictogram'] == selected_pictogram), None)
    selected_idx = selected_idx if selected_idx is not None else 0

    sim_scores = list(enumerate(similarity_matrix[selected_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    similar_pictograms = [relevant_pictograms[i[0]] for i in sim_scores[1:6]]

    popular_pictograms = sorted(similar_pictograms, key=lambda x: x['cant_used'], reverse=True)

    random.shuffle(popular_pictograms)

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
        for pic in popular_pictograms[:2]
    ]

    return {"recomendaciones": recommendations}
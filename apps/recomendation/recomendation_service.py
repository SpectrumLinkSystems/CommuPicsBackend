import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Sum
from apps.child.models.pictogram import Pictogram, PictogramUsage
from datetime import datetime

def get_pictogram_recommendations(child_id, selected_pictogram_id):
    selected_pictogram = Pictogram.objects.get(id=selected_pictogram_id)
    
    pictograms = Pictogram.objects.all()
    pictogram_data = pd.DataFrame(pictograms.values())

    pictogram_usage = PictogramUsage.objects.filter(child_id=child_id).select_related('pictogram')
    
    used_pictograms = []
    used_categories = []
    for usage in pictogram_usage:
        pictogram = usage.pictogram
        used_pictograms.append({
            'name': pictogram.name,
            'arasaac_categories': pictogram.arasaac_categories,
            'cant_used': usage.cant_used,
            'pictogram': pictogram
        })

        used_categories.extend(pictogram.arasaac_categories.split(", "))
    
    used_pictograms_df = pd.DataFrame(used_pictograms)

    if used_pictograms_df.empty:
        return {"error": "El niño no ha utilizado pictogramas previamente."}

    selected_categories = selected_pictogram.arasaac_categories.split(", ")

    relevant_pictograms = []
    for pic in used_pictograms:
        pic_categories = pic['arasaac_categories'].split(", ")
        if any(cat in pic_categories for cat in selected_categories):
            relevant_pictograms.append(pic)

    if not relevant_pictograms:
        return {"error": "No hay pictogramas relevantes para recomendar."}

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([pic['arasaac_categories'] for pic in relevant_pictograms])
    
    similarity_matrix = cosine_similarity(tfidf_matrix)

    selected_idx = relevant_pictograms.index(next(pic for pic in relevant_pictograms if pic['pictogram'] == selected_pictogram))

    sim_scores = list(enumerate(similarity_matrix[selected_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    similar_pictograms = []
    for i in sim_scores[1:6]:
        similar_pictograms.append(relevant_pictograms[i[0]])

    popular_pictograms = sorted(similar_pictograms, key=lambda x: x['cant_used'], reverse=True)
    print("POPULARIDAD",popular_pictograms)
    
    recommendations = []
    for pic in popular_pictograms[:3]:
        pictogram_data = {
            "id": pic['pictogram'].id,
            "name": pic['pictogram'].name,
            "image_url": pic['pictogram'].image_url,
            "arasaac_id": pic['pictogram'].arasaac_id,
            "arasaac_categories": pic['pictogram'].arasaac_categories,
        }
        recommendations.append({
            "child": child_id,
            "pictogram": pic['pictogram'].id,
            "pictogram_data": pictogram_data,
            "date_used": datetime.now().isoformat(),
            "cant_used": pic['cant_used']
        })

    return {"recomendaciones": recommendations}
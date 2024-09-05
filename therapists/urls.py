from django.urls import path
from .views import (
    create_therapist_view, get_all_therapists_view, get_therapist_view,
    update_therapist_view, delete_therapist_view
)

urlpatterns = [
    path('', get_all_therapists_view, name='get_all_therapists'),
    path('create/', create_therapist_view, name='create_therapist'),
    path('<int:therapist_id>/', get_therapist_view, name='get_therapist'),
    path('<int:therapist_id>/update/', update_therapist_view, name='update_therapist'),
    path('<int:therapist_id>/delete/', delete_therapist_view, name='delete_therapist'),
]
from django.urls import path
from .views import (
    create_parent_view, get_all_parents_view, get_parent_view,
    update_parent_view, delete_parent_view
)

urlpatterns = [
    path('', get_all_parents_view, name='get_all_parents'),
    path('create/', create_parent_view, name='create_parent'),
    path('<int:parent_id>/', get_parent_view, name='get_parent'),
    path('<int:parent_id>/update/', update_parent_view, name='update_parent'),
    path('<int:parent_id>/delete/', delete_parent_view, name='delete_parent'),
]

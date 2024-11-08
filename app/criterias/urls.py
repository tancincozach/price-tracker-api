# app/criterias/urls.py
from django.urls import path
from .criterias_view import CriteriaView

urlpatterns = [
    path('', CriteriaView.as_view({'get': 'get_criteria_list', 'post': 'post_criteria'}), name='criterias-list-create'),
    path('<int:pk>/', CriteriaView.as_view({'get': 'retrieve_criteria', 'delete': 'delete_criteria'}), name='criterias-detail'),
]

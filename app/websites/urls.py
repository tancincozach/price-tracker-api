# app/users/urls.py
from django.urls import path
from .websites_view import WebsitesListCreateView, WebsitesRetrieveDeleteView

urlpatterns = [
    path('', WebsitesListCreateView.as_view(), name='websites-list-create'),
    path('websites/<int:id>/', WebsitesRetrieveDeleteView.as_view(), name='websites-detail'),
]

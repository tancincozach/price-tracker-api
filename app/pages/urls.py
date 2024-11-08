# app/criterias/urls.py
from django.urls import path
from .pages_view import PagesListView

urlpatterns = [
    path('', PagesListView.as_view({'get': 'get_pages', 'post': 'post_pages'}), name='page_list_view'),
]

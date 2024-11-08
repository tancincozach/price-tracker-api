from django.urls import path
from .scraped_data_view import ScrapedDataViewSet

urlpatterns = [
    path('sync-pages/', ScrapedDataViewSet.as_view({'post': 'sync_pages'}), name='scraped_data_sync_pages'),
    path('sync-scraped-data/', ScrapedDataViewSet.as_view({'post': 'sync_scraped_data'}), name='scraped_data_sync_scraped_data'),
]

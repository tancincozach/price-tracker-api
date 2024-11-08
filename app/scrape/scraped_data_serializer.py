from rest_framework import serializers
from .scraped_data_model import ScrapedData

class ScrapedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = [
            'page', 
            'field_name', 
            'field_value', 
            'field_value_meta', 
            'date_created', 
            'updated_at', 
            'deleted_at'
        ]
        extra_kwargs = {
            'page': {'required': True},
            'field_name': {'required': True},
            'field_value': {'required': True},
            'field_value_meta': {'required': False},  # Optional for flexibility
            'date_created': {'read_only': True},
            'updated_at': {'read_only': True},
            'deleted_at': {'required': False}, 
        }

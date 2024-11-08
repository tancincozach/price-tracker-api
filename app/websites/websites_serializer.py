from rest_framework import serializers
from .websites_model import Website

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['id', 'name', 'base_url', 'created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {
            'name': {'required': True},
            'base_url': {'required': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'deleted_at': {'required': False},
        }

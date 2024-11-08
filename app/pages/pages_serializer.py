from rest_framework import serializers
from .pages_model import Page  # Adjust the import according to your project structure
from ..websites.websites_model import Website  # Import the Website model if needed

class PageSerializer(serializers.ModelSerializer):
    website_name = serializers.CharField(source='web.name', read_only=True)

    class Meta:
        model = Page
        fields = [
            'website_name',     # Add the new field here
            'url',
            'status',
            'last_scraped',
            'error_message',
            'created_at',
            'updated_at',
            'deleted_at',
        ]

    def validate_url(self, value):
        """Ensure the URL is valid."""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Invalid URL: must start with 'http://' or 'https://'.")
        return value

    def validate(self, data):
        """Additional validation can be added here if needed."""
        return data

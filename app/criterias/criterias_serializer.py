from rest_framework import serializers
from .criterias_model import Criterias
from ..websites.websites_model import Website
from ..websites.websites_serializer import WebsiteSerializer

class CriteriasSerializer(serializers.ModelSerializer):
    website = serializers.SerializerMethodField()
    
    web_id = serializers.PrimaryKeyRelatedField(
        queryset=Website.objects.all(),
        write_only=True
    )

    class Meta:
        model = Criterias
        fields = [
            'html_tag', 
            'css_selector', 
            'website',
            'web_id',
            'meta', 
            'type', 
            'created_at', 
            'updated_at', 
            'deleted_at'
        ]
        extra_kwargs = {
            'html_tag': {'required': True},
            'css_selector': {'required': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'deleted_at': {'read_only': True},
        }

    def get_website(self, obj):
        """Return the nested website details."""
        if obj.web_id:
            return WebsiteSerializer(obj.web_id).data
        return None

    def validate(self, attrs):
        """General validation for the serializer."""
        return super().validate(attrs)

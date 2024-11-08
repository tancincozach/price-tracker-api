from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from ..services.utils import Response, status, error_response, success_response, get_valid_website
from ..services.base.logger_service import LoggerService
from .criterias_model import Criterias
from .criterias_serializer import CriteriasSerializer
from ..websites.websites_model import Website

class CriteriaView(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Call the parent initializer
        self.logger_service = LoggerService(__name__)

    @action(detail=False, methods=['get'])
    def get_criteria_list(self, request):
        """
        Retrieve all criteria or filter by the specified website.
        """
        website_id = request.data.get('web_id', None)

        if website_id:
            try:
                website = get_valid_website(request.data)
                if isinstance(website, Response):
                     return website 
                queryset = Criterias.objects.filter(web_id__id=website_id)
                if not queryset.exists():
                    raise NotFound(detail="No criteria found for the specified website.")
            except Website.DoesNotExist:
                return Response({"detail": "Website not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no website ID is provided, retrieve all criteria
            queryset = Criterias.objects.all()

        serializer = CriteriasSerializer(queryset, many=True)
        self.logger_service.info("Retrieved criteria list")
        return success_response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def retrieve_criteria(self, request, pk=None):
        """
        Retrieve a specific criteria by ID.
        """
        try:
            criteria = Criterias.objects.get(id=pk)
            serializer = CriteriasSerializer(criteria)
            self.logger_service.info(f"Retrieved criteria with ID {pk}")
            return success_response(serializer.data, status.HTTP_200_OK)
        except Criterias.DoesNotExist:
            raise NotFound("Criteria not found.")
        
    @action(detail=False, methods=['post'])
    def post_criteria(self, request):
        """
        Create a new criteria.
        """
        # Validate the website ID
        website = get_valid_website(request.data)
        if isinstance(website, Response):
            return website  # Return the error response if website is invalid

        # Prepare the data for serialization
        data = request.data.copy()
        data['web_id'] = website.id
        self.logger_service.info(data)

        # Initialize the serializer with the data
        serializer = CriteriasSerializer(data=data)

        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()
            self.logger_service.info("Created new criteria")
            return success_response(serializer.data, status.HTTP_200_OK)
        
        return error_response("Invalid criteria data", errors=serializer.errors, code=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_criteria(self, request, pk=None):
        """
        Delete a specific criteria by ID.
        """
        try:
            criteria = Criterias.objects.get(id=pk)
            criteria.delete()
            self.logger_service.info(f"Deleted criteria with ID {pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Criterias.DoesNotExist:
            raise NotFound("Criteria not found.")

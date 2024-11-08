from rest_framework import viewsets
from rest_framework.decorators import action
from .pages_model import Page
from .pages_serializer import PageSerializer
from ..services.base.page_service import PageService
from ..services.base.logger_service import LoggerService
from ..services.utils import Response, status, error_response, success_response, get_valid_website

class PagesListView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger_service = LoggerService(__name__)
        self.page_service = PageService()

    @action(detail=False, methods=['get'])
    def get_pages(self, request):
        """
        :param request: The HTTP request object.
        :return: A success response containing the serialized page data.
        """
        website = get_valid_website(request.data)
        if isinstance(website, Response):
            return website
        pages = Page.objects.filter(web=website)
        serializer = PageSerializer(pages, many=True)
        return success_response({ 'pages': serializer.data }, status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def post_pages(self, request):
        """
        :param request: The HTTP request object containing URLs to process.
        :return: A success response indicating the result of the update/create operation.
        """
        website = get_valid_website(request.data)
        if isinstance(website, Response):
            return website

        urls = request.data.get('urls', [])
        if not self.is_valid_url_list(urls):
            return error_response("A valid list of URLs is required", status.HTTP_400_BAD_REQUEST)

        self.page_service.process_pages_batch(website, urls)
        return success_response({"message":"Pages successfully updated/created"},status.HTTP_200_OK)

    def is_valid_url_list(self, urls):
        """
        :param urls: A list of URLs to validate.
        :return: True if the list is valid; False otherwise.
        """
        return bool(urls) and isinstance(urls, list)

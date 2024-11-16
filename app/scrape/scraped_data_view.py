from rest_framework import viewsets
from rest_framework.decorators import action
from asgiref.sync import sync_to_async, async_to_sync
from ..websites.websites_model import Website, KABELBINDER
from ..criterias.criterias_model import Criterias
from ..services.base.logger_service import LoggerService
from ..services.scraping.kabelbinder_service import KabelBinderService
from ..services.scraping.scraped_data_service import ScrapedDataService
from ..services.base.page_service import PageService, Page
from ..services.utils import Response, status, success_response, error_response, get_valid_website

class ScrapedDataViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger_service = LoggerService(__name__)
        self.page_service = PageService()
        self.scraped_data_service = ScrapedDataService()

    def _initialize_scraper_service(self, website: Website):
        """
        :param website: The Website instance for which to initialize the scraper service.
        :return: An instance of the appropriate scraping service.
        """
        if website.name == KABELBINDER:
            return KabelBinderService()
        return ScrapedDataService()

    def _handle_sync_action(self, request, action_type):
        """
        :param request: The HTTP request object.
        :param action_type: The type of action to perform (e.g., "pages" or "scraped_data").
        :return: A success or error response based on the result of the action.
        """
        website = get_valid_website(request.data)
        if isinstance(website, Response):
            return website

        self.scraper_service = self._initialize_scraper_service(website)

        try:
            response = async_to_sync(self.process_data)(website, action_type)
            return success_response("Data synced successfully", status.HTTP_200_OK) if response else error_response("No response found", status.HTTP_404_NOT_FOUND)
        except Exception as e:
            self.logger_service.error(f"Error syncing data: {str(e)}")
            return error_response("An error occurred while syncing data", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def sync_pages(self, request):
        """
        :param request: The HTTP request object for syncing pages.
        :return: The response of the sync action for pages.
        """
        return self._handle_sync_action(request, "pages")

    @action(detail=False, methods=['post'])
    def sync_scraped_data(self, request):
        """
        :param request: The HTTP request object for syncing scraped data.
        :return: The response of the sync action for scraped data.
        """
        return self._handle_sync_action(request, "scraped_data")

    async def process_data(self, website: Website, action_type: str) -> bool:
        """
        :param website: The Website instance to process data for.
        :param action_type: The type of data to process (e.g., "pages" or "scraped_data").
        :return: A boolean indicating success or failure of the data processing.
        """
        if not self.scraper_service:
            return False

        if action_type == "pages":
            return await self.process_pages(website)
        elif action_type == "scraped_data":
            return await self.process_scraped_data(website)
        return False

    async def process_pages(self, website: Website) -> bool:
        """
        :param website: The Website instance for which pages are being processed.
        :return: A boolean indicating success or failure of the pages processing.
        """
        nav_selector = await sync_to_async(
            lambda: list(Criterias.objects.filter(web_id=website.id, type='nav').values_list('css_selector', flat=True))
        )()
        content_selectors = await sync_to_async(self.get_content_selectors)(website)
        response = await self.scraper_service.get_pages(website.base_url, nav_selector, content_selectors)
        if not response or not isinstance(response, dict):
            self.logger_service.warning(f"Invalid response received from scraper service for website: {website.name}")
            return False

        urls = self.scraper_service.extract_urls(response)
        if urls:
            await sync_to_async(self.page_service.process_pages_batch)(website, urls)
            return True

        self.logger_service.warning(f"No URLs extracted from the response for website: {website.name}")
        return False

    async def process_scraped_data(self, website: Website) -> bool:
        """
        :param website: The Website instance for which scraped data is being processed.
        :return: A boolean indicating success or failure of the scraped data processing.
        """
        if not self.scraper_service:
            return False

        content_selectors = await sync_to_async(self.get_content_selectors)(website)
        pending_pages = await sync_to_async(
            lambda: list(Page.objects.filter(
                web=website,
                status='pending',
                deleted_at__isnull=True
            ))  # Limit to 2 records
        )()

        if not pending_pages:
            self.logger_service.warning(f"No pending pages found for website: {website.name}")
            return False

        self.logger_service.info(f"Found {len(pending_pages)} pending pages for website: {website.name}")

        urls = [page.url for page in pending_pages]
        batch_size = 25

        for start in range(0, len(urls), batch_size):
            url_batch = urls[start:start + batch_size]
            if website.name == KABELBINDER:
                response = await self.scraper_service.get_data(content_selectors, url_batch)
                if response.get("data"):
                    await self._process_scraped_data_batch(pending_pages, response["data"], start)
                else:
                    self.logger_service.warning(f"No data returned for batch starting at {start} for website: {website.name}")
                self.logger_service.info(f"Response for batch starting at {start}: {response.get('data', 'No data in response')}")
            else:
                self.logger_service.warning(f"Website {website.name} is not supported for scraping.")
                return False

        return True

    async def _process_scraped_data_batch(self, pending_pages, data_batch, start):
        """
        :param pending_pages: A list of Page instances to update with scraped data.
        :param data_batch: A batch of data corresponding to the pages.
        :param start: The starting index of the current batch.
        """
        for page, resp in zip(pending_pages[start:start + 25], data_batch):
            if resp:
                scraped_data_items = [{
                    "field_name": resp.get("product", "N/A"),
                    "field_value": resp.get("price", "N/A"),
                    "field_value_meta": {"prices": resp.get("price_table", [])}
                }]
                self.logger_service.info(f"data: {scraped_data_items}")
                await sync_to_async(self.scraped_data_service.createScrapedData)(page, scraped_data_items)
                self.logger_service.info(f"Processed data for page: {page.url}")

    def get_content_selectors(self, website: Website):
        """
        :param website: The Website instance for which to retrieve content selectors.
        :return: A list of CSS selectors for content criteria associated with the website.
        """
        content_selectors = Criterias.objects.filter(web_id=website.id, type='content').values_list('css_selector', flat=True)

        return [item for selector in content_selectors for item in selector.split('|')]

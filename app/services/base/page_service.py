from django.db import transaction, IntegrityError
from ...pages.pages_model import Page
from .logger_service import LoggerService

class PageService:
    def __init__(self):
        """
        Initializes the PageService with a logger instance.
        """
        self.logger_service = LoggerService(__name__)

    def process_pages_batch(self, website, urls):
        """
        :param website: The website instance associated with the pages.
        :param urls: A list of URLs to be processed for creation or update.
        """
        created_urls = set()
        updated_urls = set()

        defaults = {
            'status': 'pending',
            'last_scraped': None,
            'error_message': None,
            'deleted_at': None,
            'updated_at': None,
        }

        try:
            # Fetch existing pages to avoid duplicates during bulk_create
            existing_pages = Page.objects.filter(url__in=urls, web=website).values_list('url', flat=True)
            new_urls = set(urls) - set(existing_pages)
            
            # Prepare pages for bulk creation
            pages_to_create = [Page(url=url, web=website, **defaults) for url in new_urls]

            # Create new pages in bulk
            if pages_to_create:
                with transaction.atomic():
                    Page.objects.bulk_create(pages_to_create)
                    created_urls.update(new_urls)

            # Update existing pages using update_or_create
            for url in existing_pages:
                try:
                    page, created = Page.objects.update_or_create(
                        url=url,
                        web=website,
                        defaults=defaults
                    )
                    if not created:
                        updated_urls.add(url)
                except Exception as e:
                    self.logger_service.error(f"Error updating page {url}: {str(e)}")

        except IntegrityError as e:
            self.logger_service.error(f"Error during bulk create: {str(e)}")

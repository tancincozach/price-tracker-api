from ...pages.pages_model import Page
from ...scrape.scraped_data_model import ScrapedData
from django.core.exceptions import ValidationError
import logging
import json

class ScrapedDataService:
    def __init__(self):
        self.logger_service = logging.getLogger(__name__)

    def createScrapedData(self, page: Page, data: list):
        """Inserts or updates scraped data records into the ScrapedData model."""
        for item in data:
            field_name = item.get('field_name', "N/A")
            field_value = item.get('field_value', "N/A")
            field_value_meta = item.get('field_value_meta', {})

            try:
                # Serialize field_value_meta to a JSON string
                field_value_meta_json = json.dumps(field_value_meta)
            except (TypeError, ValueError) as e:
                self.logger_service.error(f"Error serializing field_value_meta for {field_name}: {e}")
                field_value_meta_json = "{}"

            try:
                scraped_data, created = ScrapedData.objects.update_or_create(
                    page=page,
                    field_name=field_name,
                    defaults={
                        'field_value': field_value,
                        'field_value_meta': field_value_meta_json  # Ensure it's a JSON string
                    }
                )
                if created:
                    self.logger_service.info(f"Created new scraped data: {scraped_data}")
                else:
                    self.logger_service.info(f"Updated scraped data: {scraped_data}")
            except ValidationError as e:
                self.logger_service.error(f"Validation error while saving scraped data: {e}")

    def get_pages(self, pages: list, response: dict) -> list:
     pass

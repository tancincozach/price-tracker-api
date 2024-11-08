from ..base.abstract_web_scrape import AbstractWebScraper
from ..base.web_scrape_micro_service import WebScrapeMicroService
from ..base.logger_service import LoggerService
from urllib.parse import urlencode
import asyncio

class KabelBinderService(AbstractWebScraper):
    def __init__(self):
        super().__init__()
        self.web_scraper_service = WebScrapeMicroService()
        self.base_url = self.web_scraper_service.microservice_url
        self.website_name = 'kabelbinder'
        self.logger_service = LoggerService(__name__)
        
    def extract_sub_category_urls(self, scraped_data):
        """
        :param scraped_data: A list containing the scraped data from the website.
        :return: A list of extracted URLs.
        """
        urls = []
        for item in scraped_data:
            if 'children' in item:
                for child in item['children']:
                    if child['tag'] == 'a':
                        url = child['attributes'].get('href')
                        if url:
                            urls.append(url)
        return urls
            
    def extract_urls(self, response):
        """
        :param response: A dictionary containing pages to extract URLs from.
        :return: A list of extracted URLs.
        """
        url_array = []
        for page in response.get('pages', []):
            url = page.get('url')
            if url:
                url_array.append(url)
        return url_array

    async def fetch(self, data: dict = None):
        """
        :param data: A dictionary containing the request data.
        :return: The fetched data result from the microservice.
        """
        return await self.web_scraper_service.get_data(self.base_url, data)

    async def get_pages(self, base_url: str, classes: list, child_classes: list, additional_params: dict = {'af': 50}, batch_size: int = 25) -> dict:
        """
        :param base_url: The base URL for the initial page fetch.
        :param classes: CSS class names for elements to scrape in the main pages.
        :param child_classes: CSS class names for elements to scrape in child pages.
        :param additional_params: Additional parameters to append to URLs (default: {'af': 50}).
        :param batch_size: The number of URLs to fetch in each batch (default: 25).
        :return: A dictionary containing 'pages' with scraped data.
        """
        # Initial fetch: get the main list of pages
        result = await self.fetch({'url': base_url, 'class_name': classes})
        self.logger_service.info(f"Initial fetch result on kabelbinder service get_pages: {result}")

        # Check for valid scraped data
        if not result or 'scraped_data' not in result:
            self.logger_service.error("No valid 'scraped_data' found in results.")
            return {'pages': []}

        data = result.get('scraped_data', [])
        pages = []
        urls_to_fetch = []

        # Prepare URLs to fetch with additional parameters
        additional_query_string = urlencode(additional_params)
        for page in data:
            if 'attributes' in page:
                url = page['attributes'].get('href', '#')
                if url != '#':
                    full_url = f"{url}?{additional_query_string}"
                    urls_to_fetch.append({
                        'url': full_url,
                        'parent_name': page.get('text', 'Unknown')
                    })

        self.logger_service.info(f"URLs to fetch: {urls_to_fetch}")

        # Batch processing
        for i in range(0, len(urls_to_fetch), batch_size):
            batch = urls_to_fetch[i:i + batch_size]
            self.logger_service.info(f"Fetching for child classes: {child_classes}")
            fetch_tasks = [
                self.fetch({'url': item['url'], 'class_name': child_classes})
                for item in batch
            ]

            # Concurrently execute the fetches within the batch
            batch_results = await asyncio.gather(*fetch_tasks, return_exceptions=True)
            self.logger_service.info(f"Batch result: {batch_results}")

            # Process the results of each fetch
            for idx, product_details_result in enumerate(batch_results):
                if isinstance(product_details_result, Exception):
                    self.logger_service.error(f"Error fetching data for URL: {batch[idx]['url']} - {str(product_details_result)}")
                    continue

                product_details = product_details_result.get('scraped_data', [])
                parent_name = batch[idx]['parent_name']

                for detail in product_details:
                    product_name = detail.get('text', 'Unknown Product')
                    if detail.get('children'):
                        for product_child in detail['children']:
                            product_url = product_child['attributes'].get('href', batch[idx]['url'])
                            pages.append({
                                'name': product_name,
                                'url': product_url,
                                'parent_name': parent_name
                            })
                    else:
                        self.logger_service.error(f"No children found in product detail: {detail}")

        self.logger_service.info(f"Pages result: {pages}")
        return {'pages': pages}

    async def get_data(self, classes: list, urls: list, max_workers: int = 5) -> dict:
        """
        :param classes: CSS class names for elements to scrape in each page.
        :param urls: List of URLs to fetch data from.
        :param max_workers: The maximum number of concurrent workers (default: 5).
        :return: A dictionary containing 'data' with scraped product listings.
        """
        self.logger_service.info(f"Fetching product listings from {len(urls)} URLs.")
        results = []

        if not urls:
            self.logger_service.warning("No URLs provided for fetching products.")
            return {"data": results}
        
        queue = asyncio.Queue()
        for url in urls:
            await queue.put(url)

        async def worker():
            while not queue.empty():
                url = await queue.get()
                params = {'url': url, 'class_name': classes}
                try:
                    response = await self.fetch(params)
                    if isinstance(response, dict) and 'scraped_data' in response:
                        product_data = self.parse_response(url, classes, response)
                        if product_data:
                            results.append(product_data)
                except Exception as e:
                    self.logger_service.error(f"Error fetching data from {url}: {str(e)}")
                finally:
                    queue.task_done()

        tasks = [asyncio.create_task(worker()) for _ in range(min(max_workers, len(urls)))]

        await queue.join()
        await asyncio.gather(*tasks)

        return {"data": results}

    def parse_response(self, url: str, classes: list, response: dict) -> dict:
        """
        :param url: The URL of the page being parsed.
        :param classes: CSS class names for elements to parse in the response.
        :param response: The response data to parse.
        :return: A dictionary containing parsed product information.
        """
        if not (response and isinstance(response, dict) and 'scraped_data' in response):
            self.logger_service.warning(f"Invalid or empty response for URL: {url}.")
            return {}

        parsed_data = response['scraped_data']
        product_name = None
        main_price = None
        price_table = []

        for item in parsed_data:
            item_classes = item.get('attributes', {}).get('class', [])
            
            if item['tag'] == 'h1' and any(cls in item_classes for cls in classes['product_title']):
                product_name = item.get('text')
            elif item['tag'] == 'div' and any(cls in item_classes for cls in classes['price']):
                main_price = item.get('text')
            elif item['tag'] == 'div' and any(cls in item_classes for cls in classes['bulk_prices']):
                price_table.extend(self.parse_price_table(url, item.get('children', [])))

        if product_name and main_price and price_table:
            self.logger_service.info(f"Found bulk prices for product: {product_name}")
            return {"product": product_name, "price": main_price, "price_table": price_table}

        self.logger_service.warning(f"No bulk prices found for product: {product_name}.")
        return {}

    def parse_price_table(self, url: str, children: list) -> list:
        """
        :param url: The URL of the page containing the price table.
        :param children: The child elements containing price data.
        :return: A list of dictionaries representing the parsed prices.
        """
        prices = []
        for child in children:
            if child.get('tag') == 'div' and 'bulk' in child.get('attributes', {}).get('class', []):
                price = child.get('text')
                if price:
                    prices.append(price)
        return prices

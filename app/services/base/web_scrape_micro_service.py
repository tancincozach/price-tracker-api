import aiohttp
import asyncio
from .logger_service import LoggerService
from django.conf import settings
from tenacity import retry, stop_after_attempt, wait_fixed, RetryError
from urllib.parse import urlencode
import pybreaker

class WebScrapeMicroService:
    def __init__(self):
        self.microservice_url = f"{settings.SCRAPING_MICROSERVICE_BASE_URL}/scrape/data/"
        self.headers = {
            "Content-Type": "application/json",
            "X-Client-ID": settings.SCRAPING_MICROSERVICE_CLIENT_ID,
            "X-Client-Secret": settings.SCRAPING_MICROSERVICE_CLIENT_SECRET,
        }
        self.timeout = aiohttp.ClientTimeout(total=3600)  # 60-second timeout for requests
        self.logger_service = LoggerService(__name__)

        # Initialize the CircuitBreaker
        self.circuit_breaker = pybreaker.CircuitBreaker(
            fail_max=3,
            reset_timeout=30
        )

    def _concatenate_data_to_url(self, url_to_scrape, data):
        """
        :param url_to_scrape: The base URL to scrape.
        :param data: The additional data to be concatenated as query parameters.
        :return: The URL with query parameters concatenated.
        """
        if data:
            query_params = urlencode(data, doseq=True)
            url_with_params = f"{url_to_scrape}?{query_params}"
            return url_with_params
        return url_to_scrape

    async def _fetch_data(self, session, url_to_scrape, data=None):
        """
        :param session: The aiohttp session used for the request.
        :param url_to_scrape: The base URL to scrape.
        :param data: The additional data to be concatenated as query parameters (optional).
        :return: The JSON response from the microservice, or an error message.
        """
        url_with_params = self._concatenate_data_to_url(url_to_scrape, data)
        async with session.get(url_with_params, headers=self.headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                self.logger_service.error(f"Failed to fetch data: {response.status}, {await response.text()} from {url_with_params}")
                return {"error": f"Failed to fetch data from microservice: {response.status}"}

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))  # Retry logic for fetching data
    async def get_data(self, url_to_scrape, data=None):
        """
        :param url_to_scrape: The base URL to scrape.
        :param data: Optional data to be passed and concatenated to the URL.
        :return: The data scraped from the microservice, or an error message.
        """
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                self.logger_service.info(f"Fetching data from: {url_to_scrape}")

                fetched_data = await self.circuit_breaker.call(self._fetch_data, session, url_to_scrape, data)

                self.logger_service.info(f"Successfully fetched data from {url_to_scrape}")
                return fetched_data

        except pybreaker.CircuitBreakerError:
            self.logger_service.error(f"Circuit breaker is open. Request to {url_to_scrape} has failed.")
            return {"error": "Service unavailable due to circuit breaker open state."}
        except RetryError as e:
            self.logger_service.error(f"Max retries exceeded for {url_to_scrape}: {e}")
            return {"error": "Microservice unavailable after retries"}
        except aiohttp.ClientError as e:
            self.logger_service.error(f"Client error while connecting to microservice: {str(e)} for {url_to_scrape}")
            return {"error": str(e)}
        except asyncio.TimeoutError:
            self.logger_service.error(f"Request timed out for {url_to_scrape}")
            return {"error": "Request timed out"}
        except Exception as e:
            self.logger_service.error(f"Unexpected error while fetching data from {url_to_scrape}: {str(e)}")
            return {"error": "Unexpected error occurred"}

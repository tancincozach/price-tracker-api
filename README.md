# Price Tracker API

Price Tracker API is a tool designed for scraping and tracking the prices of products from eCommerce websites. It enables you to monitor the price fluctuations of various products over time and make informed decisions about when to purchase.

## Features
- **Scrape prices**: Fetch product prices and store them for tracking.
- **Track price history**: Retrieve historical price data of products over time.
- **Microservice integration**: Utilizes a custom-built microservice for scraping and processing the data from eCommerce websites.

## Architecture
The Price Tracker API is designed to interact with a **[**Web Data Scrape Microservice**](https://github.com/tancincozach/web-data-scrape)** that is responsible for:
- Fetching the required product information.
- Parsing and cleaning the data to provide structured price information.
- Storing the scraped data in a database.

### Web Data Scrape
The Web Data Scrape microservice provides an essential function for the Price Tracker API:
- Handles the request and response cycle for scraping eCommerce product pages.
- Returns structured data (product name, main price, price table) which the API utilizes for tracking.
  
The integration with the microservice allows the API to collect and process large batches of product data efficiently.

## Setup and Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/price-tracker-api.git
    cd price-tracker-api
    ```

2. **Install dependencies**:

    You will need Python 3.7+ and `pip` installed. Then install the required Python packages.

    ```bash
    pip install -r requirements.txt
    ```

3. **Microservice Configuration**:

    Ensure that the custom-built microservice is running and accessible by the Price Tracker API. Update the microservice URL in your settings if necessary.

4. **Database Configuration**:

    Configure the database where the scraped product data will be stored. This could be PostgreSQL, MySQL, or SQLite based on your project setup.

    ```bash
    python manage.py migrate
    ```

## Usage

To scrape product prices:

1. **Start the server**:

    ```bash
    python manage.py runserver
    ```

2. **Trigger the scraping**:

    Use the appropriate endpoints (e.g., via Postman or a custom UI) to initiate scraping. The API will fetch the prices of products from eCommerce sites, process the data, and store it for future tracking.

## Example

Example of a typical response from the API after scraping:

```json
{
  "product": "Product Name",
  "price": "19.99 €",
  "price_table": ["19.99 €", "18.99 €", "17.99 €"]
}

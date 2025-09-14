# Search Engine Crawler

This project is a web crawler built using Scrapy, designed to extract information from specified websites. It utilizes `scrapy-playwright` for handling JavaScript-rendered content, ensuring comprehensive data extraction from modern web pages.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone [repository_url]
    cd search_engine_crawler
    ```

2.  **Create and activate a Python virtual environment (Optional, for local development/testing):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies (Optional, for local development/testing):**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Spider

The `web_spider` uses default `start_urls` and `allowed_domains` defined in `search_engine_crawler/constants.py`. `sitemap_urls` can still be provided as command-line arguments.

### Running with Docker Compose (Recommended)

This project is configured to run using Docker Compose, which simplifies setup and deployment, especially with Redis for distributed crawling.

1.  **Build and run the Docker containers:**
    ```bash
    docker-compose up --build
    ```
    This command will:
    *   Build the Docker images for the `init_urls` and `crawler` services.
    *   Start a Redis server.
    *   Run `init_urls` to push initial URLs from `start_urls.txt` to Redis.
    *   Start the `crawler` service, which will begin scraping URLs from Redis.

2.  **Spawning Multiple Crawlers:**
    To run multiple instances of the crawler for increased concurrency, use the `--scale` flag:
    ```bash
    docker-compose up --build --scale crawler=3
    ```
    Replace `3` with the desired number of crawler instances.

3.  **Stopping the services:**
    ```bash
    docker-compose down
    ```

### Local Development (without Docker Compose)

To run the spider locally (without Docker Compose), ensure you have activated your virtual environment and installed dependencies.

To run the spider using the default URLs:

```bash
scrapy crawl web_spider
```

To provide `sitemap_urls` (if applicable):

```bash
scrapy crawl web_spider -a sitemap_urls="http://example.com/sitemap.xml"
```

## Project Structure

*   `scrapy.cfg`: Scrapy project configuration.
*   `search_engine_crawler/`: The main Python package for the Scrapy project.
    *   `__init__.py`: Makes `search_engine_crawler` a Python package.
    *   `settings.py`: Scrapy project settings, including middleware and pipeline configurations.
    *   `items.py`: Defines the data structure for scraped items.
    *   `pipelines.py`: Processes scraped items (e.g., saving to a database).
    *   `middlewares.py`: Custom downloader and spider middlewares.
    *   `constants.py`: Defines default `start_urls` and `allowed_domains`.
    *   `spiders/`: Directory containing the spider definitions.
        *   `__init__.py`: Makes `spiders` a Python package.
        *   `web_spider.py`: The main spider for crawling web pages, using `scrapy-playwright` for dynamic content.
*   `requirements.txt`: Lists all Python dependencies.
*   `scraped_data.db`: SQLite database for storing scraped data (if configured in pipelines).
*   `CHANGELOG.md`: Documents all notable changes to the project.
*   `Dockerfile`: Defines the Docker image for the crawler and URL initializer.
*   `docker-compose.yml`: Orchestrates the multi-container Docker application (Redis, URL initializer, crawler).
*   `init_redis_urls.sh`: Script to push initial URLs from `start_urls.txt` to Redis.
*   `start_urls.txt`: Contains the list of initial URLs for the crawler.

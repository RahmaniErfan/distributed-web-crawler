# Search Engine Crawler

This project is a web crawler built using Scrapy, designed to extract information from specified websites. It utilizes `scrapy-playwright` for handling JavaScript-rendered content, ensuring comprehensive data extraction from modern web pages.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone [repository_url]
    cd search_engine_crawler
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Spider

The `web_spider` uses default `start_urls` and `allowed_domains` defined in `search_engine_crawler/constants.py`. `sitemap_urls` can still be provided as command-line arguments.

### Example Command

To run the spider using the default URLs:

```bash
export PYTHONPATH=$PYTHONPATH:. && source venv/bin/activate && scrapy crawl web_spider
```

To provide `sitemap_urls` (if applicable):

```bash
export PYTHONPATH=$PYTHONPATH:. && source venv/bin/activate && scrapy crawl web_spider -a sitemap_urls="http://example.com/sitemap.xml"
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

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

The `web_spider` can be run with dynamic `start_urls` and `allowed_domains` provided as command-line arguments.

### Example Command

To crawl `http://quotes.toscrape.com/` and `http://books.toscrape.com/`:

```bash
source venv/bin/activate && scrapy crawl web_spider -a start_urls="http://quotes.toscrape.com/,http://books.toscrape.com/" -a allowed_domains="quotes.toscrape.com,books.toscrape.com"
```

### Simplifying the Command (PYTHONPATH)

The `export PYTHONPATH=$PYTHONPATH:"/Users/erfanrahmani/Personal Projects"` part of the command was likely added to help Python find modules if your project structure required it (e.g., if `search_engine_crawler` was importing modules from a higher-level directory like `/Users/erfanrahmani/Personal Projects`).

However, for a standard Scrapy project, if you are running the `scrapy crawl` command from within the `search_engine_crawler` directory, this `PYTHONPATH` export might not be necessary. You can try running the command without it:

```bash
source venv/bin/activate && scrapy crawl web_spider -a start_urls="http://quotes.toscrape.com/,http://books.toscrape.com/" -a allowed_domains="quotes.toscrape.com,books.toscrape.com"
```

If you encounter `ModuleNotFoundError` for your project's internal modules after removing `PYTHONPATH`, then it is indeed required for your specific setup. If it runs successfully without it, then you can safely omit that part of the command.

## Project Structure

*   `scrapy.cfg`: Scrapy project configuration.
*   `settings.py`: Scrapy project settings, including middleware and pipeline configurations.
*   `items.py`: Defines the data structure for scraped items.
*   `pipelines.py`: Processes scraped items (e.g., saving to a database).
*   `middlewares.py`: Custom downloader and spider middlewares.
*   `spiders/`: Directory containing the spider definitions.
    *   `web_spider.py`: The main spider for crawling web pages, using `scrapy-playwright` for dynamic content.
*   `requirements.txt`: Lists all Python dependencies.
*   `scraped_data.db`: SQLite database for storing scraped data (if configured in pipelines).

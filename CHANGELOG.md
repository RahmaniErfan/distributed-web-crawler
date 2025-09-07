# Changelog

All notable changes to this project will be documented in this file.
Initial commits were accidentally deleted, please refer to initial changes in this file.
## [Unreleased]

### Added
-   **Externalized Spider Configuration**: The `web_spider` now accepts `start_urls`, `allowed_domains`, and `sitemap_urls` as command-line arguments, making the spider more flexible and reusable without code modifications.
-   **SQLite Data Storage Pipeline**: A new `SearchEngineCrawlerPipeline` has been implemented to store scraped items into a `scraped_data.db` SQLite database. This provides persistent and queryable storage for the extracted data. The pipeline also handles duplicate URLs.
-   **Proxy Rotation Middleware (Optional)**: A `ProxyMiddleware` was added to `middlewares.py` and enabled in `settings.py` (commented out by default) to allow for rotating proxies, enhancing robustness against anti-bot measures.
-   **Data Cleaning Method**: A `clean_body` method was added to `items.py` to remove excessive whitespace from extracted body text, and integrated into `web_spider.py`.
-   **Scrapy Monitoring Extensions**: Enabled `LogStats` and `CoreStats` extensions in `settings.py` for better crawl statistics and monitoring.

### Changed
-   **Dynamic Conditional Playwright Usage**: Modified `web_spider.py` to intelligently determine when to use Playwright. Initial requests are made without Playwright, and it's only re-requested with Playwright if the response indicates JavaScript-heavy content or a redirect, optimizing resource usage.
-   **Enhanced SQLite Pipeline**: The `SearchEngineCrawlerPipeline` in `pipelines.py` now includes basic data validation (checking for missing URLs) and more robust error handling for SQLite operations, including rollback on errors and more informative logging.

### Fixed
-   **`TypeError: 'async_generator' object is not iterable`**: Resolved this runtime error by adjusting the `start_requests` method in `web_spider.py` to be a synchronous generator, compatible with `SitemapSpider`'s internal workings.
-   **`ModuleNotFoundError: No module named 'search_engine_crawler'`**: Diagnosed and provided the correct command to run the spider by explicitly setting the `PYTHONPATH` to include the project's parent directory.

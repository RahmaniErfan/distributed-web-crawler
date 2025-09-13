# Changelog

All notable changes to this project will be documented in this file.
Initial commits were accidentally deleted, please refer to initial changes in this file.
## [Unreleased]

### Added
-   **Performance Control Settings**: Added `PLAYWRIGHT_ENABLED`, `PLAYWRIGHT_MAX_RETRIES`, and `DEPTH_LIMIT` to `settings.py` for fine-grained control over crawling behavior and resource usage.
-   **Centralized Default URLs**: Moved default `start_urls` and `allowed_domains` to `search_engine_crawler/constants.py` for easier management.
-   **Externalized Spider Configuration**: The `web_spider` now accepts `sitemap_urls` as command-line arguments, making the spider more flexible and reusable without code modifications. `start_urls` and `allowed_domains` are now exclusively managed via `constants.py`.
-   **SQLite Data Storage Pipeline**: A new `SearchEngineCrawlerPipeline` has been implemented to store scraped items into a `scraped_data.db` SQLite database. This provides persistent and queryable storage for the extracted data. The pipeline also handles duplicate URLs.
-   **Proxy Rotation Middleware (Optional)**: A `ProxyMiddleware` was added to `middlewares.py` and enabled in `settings.py` (commented out by default) to allow for rotating proxies, enhancing robustness against anti-bot measures.
-   **Data Cleaning Method**: A `clean_body` method was added to `items.py` to remove excessive whitespace from extracted body text, and integrated into `web_spider.py`.
-   **Scrapy Monitoring Extensions**: Enabled `LogStats` and `CoreStats` extensions in `settings.py` for better crawl statistics and monitoring.

### Changed
-   **Refined Playwright Heuristic**: Updated `web_spider.py` to use the new `PLAYWRIGHT_ENABLED` and `PLAYWRIGHT_MAX_RETRIES` settings, and improved the heuristic for determining when Playwright is needed, reducing unnecessary browser rendering.
-   **Depth Limiting**: Integrated `DEPTH_LIMIT` from `settings.py` into `web_spider.py` to control the maximum crawling depth.
-   **Expanded Default URLs**: Increased the number of default `start_urls` and `allowed_domains` in `search_engine_crawler/constants.py`.
-   **Dynamic Conditional Playwright Usage**: Modified `web_spider.py` to intelligently determine when to use Playwright. Initial requests are made without Playwright, and it's only re-requested with Playwright if the response indicates JavaScript-heavy content or a redirect, optimizing resource usage.
-   **Enhanced SQLite Pipeline**: The `SearchEngineCrawlerPipeline` in `pipelines.py` now includes basic data validation (checking for missing URLs) and more robust error handling for SQLite operations, including rollback on errors and more informative logging.

### Fixed
-   **`TypeError: 'async_generator' object is not iterable`**: Resolved this runtime error by adjusting the `start_requests` method in `web_spider.py` to be a synchronous generator, compatible with `SitemapSpider`'s internal workings.
-   **`ModuleNotFoundError: No module named 'search_engine_crawler.settings'`**: Resolved by correcting the project structure (moving core files into `search_engine_crawler/`) and providing the correct `PYTHONPATH` export command.
-   **`ValueError: Missing scheme in request url`**: Fixed by filtering out non-HTTP/HTTPS links in `web_spider.py` using `urllib.parse.urlparse`.

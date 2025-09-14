# Scrapy settings for search_engine_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "search_engine_crawler"

SPIDER_MODULES = ["search_engine_crawler.spiders"]
NEWSPIDER_MODULE = "search_engine_crawler.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "search_engine_crawler (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Scrapy-Redis settings
# Enables scheduling storing requests queue in Redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share a common duplication filter through Redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Don't cleanup Redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True

# Default Redis connection settings.
# Default Redis connection settings.
# These will be overridden by environment variables in Docker Compose
REDIS_HOST = 'redis' 
REDIS_PORT = 6379

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 32 # Increased for better performance, adjust as needed
CONCURRENT_REQUESTS_PER_DOMAIN = 8 # Allow more concurrent requests per domain
DOWNLOAD_DELAY = 0.5 # Reduced initial delay, AutoThrottle will manage it

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 8.0 # Target 8 concurrent requests per domain
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "search_engine_crawler.middlewares.SearchEngineCrawlerSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "search_engine_crawler.middlewares.SearchEngineCrawlerDownloaderMiddleware": 543,
}

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
PLAYWRIGHT_BROWSER_TYPE = 'chromium' # or 'firefox' or 'webkit'
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': True, # Run in headless mode
    'timeout': 10000, # 10 seconds
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000 # 30 seconds
PLAYWRIGHT_MAX_PAGES_PER_BROWSER = 5 # Max 5 pages per browser instance
PLAYWRIGHT_ENABLED = True # Global switch to enable/disable Playwright
PLAYWRIGHT_MAX_RETRIES = 1 # Max retries for a request with Playwright if it fails

# Crawling depth limit
DEPTH_LIMIT = 5 # Increased limit to allow deeper crawling

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
    "scrapy.extensions.logstats.LogStats": 100, # Enable LogStats extension
    "scrapy.extensions.corestats.CoreStats": 100, # Enable CoreStats extension
    # "search_engine_crawler.extensions.CustomMonitoringExtension": 500, # Future custom extension
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "search_engine_crawler.pipelines.SearchEngineCrawlerPipeline": 300,
    "scrapy_redis.pipelines.RedisPipeline": 400, # Add RedisPipeline to store items in Redis
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Proxy settings (optional)
# PROXY_LIST = [
#     'http://proxy1.com:8000',
#     'http://proxy2.com:8000',
#     'http://user:pass@proxy3.com:8000',
# ]

# Enable our custom proxy middleware
DOWNLOADER_MIDDLEWARES.update({
    'search_engine_crawler.middlewares.ProxyMiddleware': 100,
})

# Logging settings
LOG_LEVEL = 'DEBUG' # DEBUG, INFO, WARNING, ERROR, CRITICAL
# LOG_FILE = 'scrapy.log' # Uncomment to enable logging to a file

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"

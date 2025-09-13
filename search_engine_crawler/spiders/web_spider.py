import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.utils.project import get_project_settings
from ..items import SearchEngineCrawlerItem
from ..constants import DEFAULT_START_URLS, DEFAULT_ALLOWED_DOMAINS
from urllib.parse import urlparse # Import urlparse

class WebSpider(SitemapSpider):
    name = 'web_spider'
    
    allowed_domains = []
    start_urls = []
    sitemap_urls = []
    
    settings = get_project_settings()
    PLAYWRIGHT_ENABLED = settings.getbool('PLAYWRIGHT_ENABLED', True)
    PLAYWRIGHT_MAX_RETRIES = settings.getint('PLAYWRIGHT_MAX_RETRIES', 1)
    DEPTH_LIMIT = settings.getint('DEPTH_LIMIT', 0) # 0 means no limit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize with default values from constants.py
        self.start_urls = list(DEFAULT_START_URLS)
        self.allowed_domains = list(DEFAULT_ALLOWED_DOMAINS)
        self.sitemap_urls = [] # Sitemap URLs don't have a default

        # Only sitemap_urls can be overridden via command-line arguments
        if 'sitemap_urls' in kwargs:
            self.sitemap_urls = kwargs.get('sitemap_urls').split(',')

    def start_requests(self):
        # Initial requests without Playwright, depth 0
        if self.start_urls:
            for url in self.start_urls:
                yield scrapy.Request(url, self.parse, meta={'depth': 0})
        elif self.sitemap_urls:
            for sitemap_url in self.sitemap_urls:
                yield scrapy.Request(sitemap_url, self._parse_sitemap, meta={'depth': 0})
        else:
            self.logger.warning("No start_urls or sitemap_urls provided. Spider will not start.")

    async def parse(self, response):
        current_depth = response.meta.get('depth', 0)

        # Check depth limit
        if self.DEPTH_LIMIT and current_depth > self.DEPTH_LIMIT:
            self.logger.debug(f"Depth limit reached for {response.url} at depth {current_depth}")
            return

        # Determine if Playwright should be used
        use_playwright = False
        playwright_retries = response.meta.get('playwright_retries', 0)

        if self.PLAYWRIGHT_ENABLED:
            if response.meta.get('playwright_priority'):
                use_playwright = True
                self.logger.debug(f"Playwright prioritized for {response.url}")
            elif response.meta.get('playwright_used'):
                # If Playwright was already used for this request, continue with it
                use_playwright = True
                self.logger.debug(f"Parsing with Playwright for {response.url} (already used)")
            else:
                # Heuristic to determine if Playwright is needed for the first time
                # More specific checks for JavaScript-heavy content
                content_type = response.headers.get('Content-Type', b'').decode('utf-8').lower()
                if 'text/html' in content_type:
                    # Check for common SPA patterns or very minimal HTML
                    if not response.text or len(response.text.strip()) < 200: # Very small response
                        use_playwright = True
                    elif 'window.location.replace' in response.text or 'window.location.href' in response.text: # JS redirect
                        use_playwright = True
                    elif 'react-root' in response.text or 'vue-app' in response.text or 'ng-app' in response.text: # Common SPA markers
                        use_playwright = True
                
                if use_playwright and playwright_retries < self.PLAYWRIGHT_MAX_RETRIES:
                    self.logger.info(f"Retrying with Playwright for {response.url} (retry {playwright_retries + 1}) due to JavaScript-heavy content.")
                    yield scrapy.Request(
                        response.url,
                        self.parse,
                        meta={
                            'playwright': True,
                            'playwright_used': True,
                            'playwright_retries': playwright_retries + 1,
                            'depth': current_depth # Maintain depth
                        },
                        dont_filter=True # Important to allow re-requesting the same URL
                    )
                    return # Do not proceed with extraction in this branch

        if use_playwright:
            self.logger.debug(f"Parsing with Playwright for {response.url}")
        else:
            self.logger.debug(f"Parsing without Playwright for {response.url}")

        async for item_or_request in self._extract_and_follow(response, current_depth):
            yield item_or_request

    async def _extract_and_follow(self, response, current_depth):
        item = SearchEngineCrawlerItem()
        item['url'] = response.url
        item['title'] = response.css('title::text').get()
        raw_body = ' '.join(response.css('body *::text').getall())
        item['body'] = item.clean_body(raw_body)
        item['description'] = response.css('meta[name="description"]::attr(content)').get()
        item['keywords'] = response.css('meta[name="keywords"]::attr(content)').get()
        
        # Extract all outgoing links
        item['outgoing_links'] = response.css('a::attr(href)').getall()

        yield item

        # Follow all links on the page to continue crawling
        next_depth = current_depth + 1
        if self.DEPTH_LIMIT and next_depth > self.DEPTH_LIMIT:
            self.logger.debug(f"Not following links from {response.url}: depth limit {self.DEPTH_LIMIT} reached for next depth {next_depth}")
            return

        for href in response.css('a::attr(href)').getall():
            parsed_url = urlparse(href)
            # Filter out non-HTTP/HTTPS links (e.g., mailto:, javascript:)
            if parsed_url.scheme in ['http', 'https']:
                # Pass playwright_used meta to ensure subsequent requests from this page
                # also consider conditional playwright usage
                meta = {
                    'depth': next_depth,
                    'playwright_used': response.meta.get('playwright_used', False),
                    'playwright_retries': 0 # Reset retries for new requests
                }
                yield response.follow(href, self.parse, meta=meta)
            else:
                self.logger.debug(f"Skipping non-HTTP/HTTPS link with scheme: {parsed_url.scheme} for URL: {href}")

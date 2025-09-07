import scrapy
from scrapy.spiders import SitemapSpider
from ..items import SearchEngineCrawlerItem

class WebSpider(SitemapSpider):
    name = 'web_spider'
    # Allowed domains will be dynamically populated or configured.
    # For now, we'll keep it broad or specify a few examples.
    # allowed_domains and start_urls will be set via custom_settings or spider arguments
    # For now, we'll keep them as empty lists or provide a default if needed.
    allowed_domains = []
    start_urls = []
    sitemap_urls = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'start_urls' in kwargs:
            self.start_urls = kwargs.get('start_urls').split(',')
        if 'allowed_domains' in kwargs:
            self.allowed_domains = kwargs.get('allowed_domains').split(',')
        if 'sitemap_urls' in kwargs:
            self.sitemap_urls = kwargs.get('sitemap_urls').split(',')

    def start_requests(self): # Reverted to synchronous generator for SitemapSpider compatibility
        # Initial requests without Playwright
        if self.start_urls:
            for url in self.start_urls:
                yield scrapy.Request(url, self.parse)
        elif self.sitemap_urls:
            for sitemap_url in self.sitemap_urls:
                yield scrapy.Request(sitemap_url, self._parse_sitemap)
        else:
            self.logger.warning("No start_urls or sitemap_urls provided. Spider will not start.")

    async def parse(self, response):
        # Check if Playwright was already used for this request
        if response.meta.get('playwright_used'):
            self.logger.debug(f"Parsing with Playwright for {response.url}")
            # Proceed with extraction as Playwright has already rendered the page
            async for item_or_request in self._extract_and_follow(response):
                yield item_or_request
        else:
            # Heuristic to determine if Playwright is needed
            # Check for minimal HTML content or common JavaScript redirects
            is_javascript_heavy = False
            if not response.text or len(response.text.strip()) < 500: # Very small response
                is_javascript_heavy = True
            elif '<script>' in response.text.lower() and 'document.location' in response.text.lower(): # JS redirect
                is_javascript_heavy = True
            elif 'window.location' in response.text.lower() and 'href' in response.text.lower(): # JS redirect
                is_javascript_heavy = True
            # Add more heuristics as needed

            if is_javascript_heavy:
                self.logger.info(f"Retrying with Playwright for {response.url} due to JavaScript-heavy content.")
                yield scrapy.Request(
                    response.url,
                    self.parse,
                    meta={'playwright': True, 'playwright_used': True},
                    dont_filter=True # Important to allow re-requesting the same URL
                )
            else:
                self.logger.debug(f"Parsing without Playwright for {response.url}")
                async for item_or_request in self._extract_and_follow(response):
                    yield item_or_request

    async def _extract_and_follow(self, response):
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
        for href in response.css('a::attr(href)').getall():
            # Pass playwright_used meta to ensure subsequent requests from this page
            # also consider conditional playwright usage
            meta = {'playwright_used': True} if response.meta.get('playwright_used') else {}
            yield response.follow(href, self.parse, meta=meta)
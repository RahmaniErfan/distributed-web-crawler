import scrapy

class SearchEngineCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    outgoing_links = scrapy.Field()

    def clean_body(self, body_text):
        """Removes excessive whitespace and cleans the body text."""
        if body_text:
            # Replace multiple spaces/newlines/tabs with a single space
            cleaned_text = ' '.join(body_text.split())
            return cleaned_text.strip()
        return body_text

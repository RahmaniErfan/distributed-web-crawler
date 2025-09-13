import sqlite3
from itemadapter import ItemAdapter

class SearchEngineCrawlerPipeline:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open_spider(self, spider):
        self.conn = sqlite3.connect('scraped_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                body TEXT,
                description TEXT,
                keywords TEXT,
                outgoing_links TEXT
            )
        ''')
        self.conn.commit()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Basic data validation/cleaning within the pipeline
        if not adapter.get('url'):
            spider.logger.warning(f"Item missing URL, skipping: {item}")
            return item # Or raise DropItem("Missing URL")

        try:
            self.cursor.execute('''
                INSERT INTO pages (url, title, body, description, keywords, outgoing_links)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                adapter['url'],
                adapter['title'],
                adapter['body'],
                adapter['description'],
                adapter['keywords'],
                ','.join(adapter['outgoing_links']) if adapter['outgoing_links'] else ''
            ))
            self.conn.commit()
            spider.logger.debug(f"Item stored: {adapter['url']}")
        except sqlite3.IntegrityError:
            spider.logger.info(f"Duplicate entry for URL: {adapter['url']}")
        except Exception as e:
            spider.logger.error(f"Error storing item {adapter['url']}: {e}")
            self.conn.rollback() # Rollback in case of other errors
        return item

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()
            spider.logger.info("SQLite connection closed.")

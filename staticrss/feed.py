import re
import logging
import dateutil.parser
import datetime
import pytz


class Storage(object):
    def __init__(self, backend):
        self.backend = backend

    def update(self, url, items):
        """Add a list of *items* of type feed.Item for a given *url*.
        
        If an item with the same link already exists it is *not* updated. This
        happens when an RSS/Atom feed does not contain a valid publish date.
        """
        if url not in self.backend:
            self.backend[url] = items
            return

        old_items = self.backend[url]
        old_links = set((item.link for item in old_items))
        new_links = set((item.link for item in items))

        for link in (new_links - old_links):
            logging.info("Found {0}".format(link))

            # Okay, this stinks. But we have time ...
            for item in items:
                if link == item.link:
                    old_items.append(item)

        self.backend[url] = old_items

    def items(self):
        """Yield *all* feed items."""
        for k, v in self.backend.items():
            for item in v:
                yield item

    def __getitem__(self, url):
        return self.backend[url]


class Item(object):
    """
    The canonical representation of a feed item to be used in the Jinja
    templates.

    It supports the following attributes:

        - title: The title of the item
        - link: A URL to the item
        - age: Age of this item compared to now, as a timedelta
        - channel_title: The title of the associated "channel" or site
        - content: Content with HTML tags
        - clean: Content without HTML tags
    """

    today = pytz.UTC.localize(datetime.datetime.today())

    def __init__(self, parsed_item, feed):
        self.published = self.today

        for attr in ('updated', 'published', 'pubDate'):
            if hasattr(parsed_item, attr):
                date = getattr(parsed_item, attr)
                try:
                    self.published = dateutil.parser.parse(date)
                except:
                    pass

        try:
            self.published = pytz.UTC.localize(self.published)
        except:
            pass

        self.title = parsed_item.title
        self.link = parsed_item.link
        self.age = self.today - self.published
        self.channel_title = feed.channel.title

        try:
            self.content = parsed_item.content[0].value
            self.clean = re.sub('<[^<]+?>', '', self.content)
        except AttributeError:
            self.content = ""
            self.clean = ""

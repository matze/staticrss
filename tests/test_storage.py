import unittest
import datetime
import pytz
import staticrss.feed


class Item(object):
    def __init__(self, link, title, published=None):
        self.link = link
        self.title = title
        self.published = published
        self.age = None


class TestStorage(unittest.TestCase):
    def setUp(self):
        published = datetime.datetime.today() - datetime.timedelta(days=1)
        self.first_item = Item('foo.com/bar.html', 'Foobar',
                               pytz.UTC.localize(published))
        self.url = 'foo.com'
        self.backend = {self.url: [self.first_item]}
        self.storage = staticrss.feed.Storage(self.backend)

    def test_add_item_to_existing_url(self):
        item = Item('foo.com/baz.html', 'Foobaz')

        self.assertEqual(len(self.storage[self.url]), 1)
        self.storage.update(self.url, [item])
        self.assertEqual(len(self.storage[self.url]), 2)

    def test_add_same_item(self):
        self.assertEqual(len(self.storage[self.url]), 1)
        self.storage.update(self.url, [self.first_item])
        self.assertEqual(len(self.storage[self.url]), 1)

    def test_iterate(self):
        item = Item('bar.co.uk/baz.html', 'Foobaz')
        self.storage.update('bar.co.uk', [item])

        for item in self.storage.items():
            assert item.link in ('bar.co.uk/baz.html', 'foo.com/bar.html')

    def test_update_age(self):
        published = datetime.datetime.today() - datetime.timedelta(days=2)
        item = Item('xyz', 'What', pytz.UTC.localize(published))
        self.storage.update('bloerg.net', [item])
        self.storage.update_age()
        self.assertEqual(item.age.days, 2)

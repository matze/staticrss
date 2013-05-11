import unittest
import staticrss.feed


class Item(object):
    def __init__(self, link, title):
        self.link = link
        self.title = title


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.first_item = Item('foo.com/bar.html', 'Foobar')
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

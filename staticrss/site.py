import os
import shutil
import logging
import feedcache
import jinja2
import shelve
import staticrss.feed


def _copyable_files(extension):
    return (path for path in os.listdir('.')
            if not path.startswith('_') and path.endswith(extension))


def _update_feeds(feed_urls, storage):
    """Read urls from *feed_urls* and update the *storage*"""
    cache_storage = shelve.open('.cache')
    cache = feedcache.Cache(cache_storage)

    for url in feed_urls:
        logging.info("Fetching {0}".format(url))
        feed = cache.fetch(url)
        items = [staticrss.feed.Item(item, feed) for item in feed.entries]
        storage.update(url, items)

    cache_storage.close()


def _get_sorted_feed_entries(storage):
    entries = [item for item in storage.items()]
    return sorted(entries, key=lambda item: item.age)


def _fwalk(root, predicate):
    for path, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if predicate(d)]
        yield path, dirnames, filenames


def _process_files(config, storage, env):
    entries = _get_sorted_feed_entries(storage)

    dest = config['destination']
    predicate = lambda d: not d.startswith('_')

    for path, dirs, files in _fwalk(config['source'], predicate):
        dest_dir = os.path.join(dest, path)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for filename in files:
            if not filename.startswith(('.', '_')):
                src = os.path.join(path, filename)
                dst = os.path.join(dest_dir, filename)

                if filename.endswith('.html'):
                    template = env.get_template(src)

                    with open(dst, 'w') as f:
                        html = template.render(entries=entries)
                        f.write(html.encode('utf-8'))
                else:
                    src = os.path.join(path, filename)
                    dst = os.path.join(dest_dir, filename)
                    shutil.copy(src, dst)


def build(config):
    loader = jinja2.FileSystemLoader([config['layouts'], '.'])
    env = jinja2.Environment(loader=loader)

    storage_backend = shelve.open('.storage')
    storage = staticrss.feed.Storage(storage_backend)

    _update_feeds(config['feeds'], storage)
    _process_files(config, storage, env)

    storage_backend.close()
